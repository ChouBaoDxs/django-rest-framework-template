import datetime
import logging
import os

import opentracing
import six
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from jaeger_client.config import Config, Tracer
from jaeger_client.constants import TRACE_ID_HEADER as DEFAULT_TRACE_ID_HEADER
from opentracing import Format
from opentracing.ext import tags

"""
jaeger-client-python：https://github.com/jaegertracing/jaeger-client-python，已经废弃，官方建议迁移到 OpenTelemetry

本地测试开发启动 jaeger docker：
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest
  
访问： http://localhost:16686
"""

# global jaeger config
JAEGER_SERVICE_NAME = os.getenv('JAEGER_SERVICE_NAME', "default_jaeger_service_name")
# TRACE_ID_HEADER = os.getenv('TRACE_ID_HEADER', DEFAULT_TRACE_ID_HEADER)
TRACE_ID_HEADER = os.getenv('TRACE_ID_HEADER', 'trace-id')
OPERATION_NAME = os.getenv('OPERATION_NAME', "default_operation_name")


def format_request_headers(request_meta):
    headers = {}
    for k, v in six.iteritems(request_meta):
        k = k.lower().replace('_', '-')
        if k.startswith('http-'):
            k = k[5:]
            headers[k] = v
    return headers


def format_hex_trace_id(trace_id: int):
    return '{:x}'.format(trace_id)


def init_jaeger_tracer() -> Tracer:
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            # 'local_agent': {
            #     'reporting_host': 'your-reporting-host',
            #     'reporting_port': 'your-reporting-port',
            # },
        },
        service_name=JAEGER_SERVICE_NAME,
    )
    tracer = config.initialize_tracer()
    return tracer


"""
# https://github.com/GalphaXie/django-jaeger-middleware
class JaegerMiddleWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.extract_request_ctx(request)
        response = self.get_response(request)
        response[TRACE_ID_HEADER] = request.META.get(TRACE_ID_HEADER, "")
        return response

    def inject_span(self, span, request: HttpRequest):
        span.set_tag(tags.HTTP_METHOD, request.method)
        span.set_tag(tags.HTTP_URL, request.path)
        span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
        tracer.inject(span, Format.HTTP_HEADERS, request.META)

    def extract_request_ctx(self, request: HttpRequest):
        span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
        span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
        with tracer.start_span(operation_name=OPERATION_NAME, child_of=span_ctx, tags=span_tags) as gate_span:
            self.inject_span(gate_span, request)

    def process_request(self, request):
        pass
"""


# https://blog.csdn.net/pushiqiang/article/details/114449564
def before_request_trace(tracer, request, view_func):
    """
    Helper function to avoid rewriting for middleware and decorator.
    Returns a new span from the request with logged attributes and
    correct operation name from the view_func.
    """
    # strip headers for trace info
    headers = format_request_headers(request.META)

    # start new span from trace info
    operation_name = view_func.__name__
    try:
        span_ctx = tracer.extract(opentracing.Format.HTTP_HEADERS, headers)
        scope = tracer.start_active_span(operation_name, child_of=span_ctx)
    except (opentracing.InvalidCarrierException,
            opentracing.SpanContextCorruptedException):
        scope = tracer.start_active_span(operation_name)

    span = scope.span
    span.set_tag(tags.COMPONENT, 'Django')
    # span.set_tag(tags.TRACE_ID, format_hex_trace_id(span.trace_id))
    span.set_tag(TRACE_ID_HEADER, format_hex_trace_id(span.trace_id))
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
    span.set_tag(tags.HTTP_METHOD, request.method)
    span.set_tag(tags.HTTP_URL, request.get_full_path())

    # request_id = headers.get(tags.REQUEST_ID)
    request_id = headers.get('request-id')
    if request_id:
        # span.set_tag(tags.REQUEST_ID, request_id)
        span.set_tag('request-id', request_id)

    request.scope = scope

    return scope


def after_request_trace(request, response=None, error=None):
    scope = getattr(request, 'scope', None)

    if scope is None:
        return

    if response is not None:
        scope.span.set_tag(tags.HTTP_STATUS_CODE, response.status_code)
    if error is not None:
        scope.span.set_tag(tags.ERROR, True)
        scope.span.log_kv({
            'event': tags.ERROR,
            'error.kind': type(error),
            'error.object': error,
            'error.stack': error.__traceback__,
            'request.headers': format_request_headers(request.META),
            'request.args': request.GET,
            'request.data': request.POST
        })

    scope.close()


def trace(tracer):
    """
    # 链路追踪装饰器
    """

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            before_request_trace(tracer, request, view_func)
            try:
                response = view_func(request, *args, **kwargs)
            except Exception as e:
                after_request_trace(request, error=e)
                raise e
            else:
                after_request_trace(request, response)

            return response

        wrapper.__name__ = view_func.__name__
        return wrapper

    return decorator


class JaegerMiddleWare(MiddlewareMixin):
    def __init__(self, get_response=None):
        self._init_tracer()
        self.get_response = get_response

    def _init_tracer(self):
        self.tracer = init_jaeger_tracer()

    def process_view(self, request, view_func, view_args, view_kwargs):
        before_request_trace(self.tracer, request, view_func)

    def process_exception(self, request, exception):
        after_request_trace(request, error=exception)

    def process_response(self, request, response):
        after_request_trace(request, response=response)
        return response


class ErrorTraceHandler(logging.Handler):
    """
    Custom ErrorTraceHandlerimplementation to forward python logger records to Jaeger / OpenTracing
    """

    def __init__(self, level=logging.ERROR):
        """
        Initialize the handler.
        """
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            operation_name = 'logger[{}]'.format(record.name)
            parent_span = opentracing.tracer.active_span
            if not parent_span:
                return
            with opentracing.tracer.start_span(operation_name, child_of=parent_span) as logger_span:
                logger_span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_LOG)
                logger_span.set_tag(tags.LOGGER, record.name)

                logger_span.log_kv({
                    'event': tags.LOG_ERROR,
                    'message': msg,
                    'log.stack_info': record.stack_info,
                    'log.asctime': getattr(record, 'asctime', datetime.datetime.now()),
                    'log.created': record.created,
                    'log.filename': record.filename,
                    'log.funcName': record.funcName,
                    'log.levelname': record.levelname,
                    'log.lineno': record.lineno,
                    'log.module': record.module,
                    'log.msecs': record.msecs,
                    'log.name': record.name,
                    'log.pathname': record.pathname,
                    'log.process': record.process,
                    'log.thread': record.thread
                })
        except Exception as e:
            self.handleError(record)
