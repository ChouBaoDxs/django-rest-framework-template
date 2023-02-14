import os

from opentelemetry import trace
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import BatchSpanProcessor

OTEL_PYTHON_DJANGO_INSTRUMENT = os.getenv('OTEL_PYTHON_DJANGO_INSTRUMENT', 'True').lower() == 'true'  # 源码里有 environ.get(OTEL_PYTHON_DJANGO_INSTRUMENT) == "False"


def init_tracer():
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: "my-helloworld-service"})
        )
    )
    tracer = trace.get_tracer(__name__)

    # create a JaegerExporter
    jaeger_exporter = JaegerExporter(
        # configure agent
        agent_host_name='localhost',
        agent_port=6831,
        # optional: configure also collector
        # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
        # username=xxxx, # optional
        # password=xxxx, # optional
        # max_tag_value_length=None # optional
    )

    # Create a BatchSpanProcessor and add the exporter to it
    span_processor = BatchSpanProcessor(jaeger_exporter)

    # add to the tracer
    provider: TracerProvider = trace.get_tracer_provider()
    provider.add_span_processor(span_processor)


if OTEL_PYTHON_DJANGO_INSTRUMENT:
    init_tracer()


    # https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/django/django.html
    def request_hook(span, request):
        # https://github.com/open-telemetry/opentelemetry-python-contrib/issues/288
        activation_key = "opentelemetry-instrumentor-django.activation_key"
        if activation_key in request.META:
            request.META[activation_key].__name__ = ""


    def response_hook(span, request, response):
        pass


    DjangoInstrumentor().instrument(request_hook=request_hook, response_hook=response_hook)
