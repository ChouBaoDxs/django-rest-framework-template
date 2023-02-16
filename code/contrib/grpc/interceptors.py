import json
from typing import Any, Callable

import grpc
from django_socio_grpc.exceptions import GRPCException
from google.protobuf.json_format import MessageToDict
from grpc_interceptor import ServerInterceptor
from opentelemetry import trace
from opentelemetry.sdk.trace import Span


class Interceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        rsp = continuation(handler_call_details)
        return rsp


class ExceptionInterceptor(ServerInterceptor):
    def intercept(
            self,
            method: Callable,
            request: Any,
            context: grpc.ServicerContext,
            method_name: str,
    ) -> Any:
        try:
            return method(request, context)
        except Exception as e:
            raise


class TraceRequestDataInterceptor(ServerInterceptor):
    """
    这个拦截器用于将请求数据设置给 trace
    """

    def intercept(
            self,
            method: Callable,
            request: Any,
            context: grpc.ServicerContext,
            method_name: str,
    ) -> Any:
        span: Span = trace.get_current_span()
        if span.is_recording():
            try:
                request_data = MessageToDict(request)
                request_data_str = json.dumps(request_data, ensure_ascii=False)
                # 避免请求数据过大，这里无脑剪切一下
                request_data_str = request_data_str[:100]
                span.set_attribute('request.data', request_data_str)
            except Exception as e:
                span.set_attribute('set_request_data_err', str(e))

        response = method(request, context)
        # response_data = MessageToDict(response)
        return response
