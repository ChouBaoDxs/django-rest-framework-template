import json
import logging
import time

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import underscoreize
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail

error_logger = logging.getLogger("error")


class GetParamsCamelCaseMiddleware:
    """
    get 参数 params 驼峰转下划线中间件
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.GET = underscoreize(
            request.GET,
            **api_settings.JSON_UNDERSCOREIZE
        )

        response = self.get_response(request)
        return response


class CodeMessageDataMiddleware(MiddlewareMixin):
    """
    封装 code message data 响应
    """

    def process_request(self, request):
        pass

    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass

    def process_template_response(self, request, response):
        if request.path.startswith(('/swagger', '/docs')):
            return response

        if hasattr(response, 'data'):
            data = {'code': 200, 'message': 'ok', 'data': response.data}
            try:
                if response.status_code < 400:
                    pass
                else:
                    data['code'] = response.status_code
                    data['message'] = 'fail'
                    if isinstance(response.data, dict):
                        detail = response.data.get('detail')
                        if detail:
                            data['message'] = str(detail)
                        else:
                            for k, v in response.data.items():
                                if v and isinstance(v, list) and isinstance(v[0], ErrorDetail):
                                    data['message'] = str(v[0])
                                    break
                    elif type(response.data) == list:
                        if response.data:
                            if type(response.data[0]) == ErrorDetail:
                                data['message'] = str(response.data[0])
            except Exception as e:
                data['code'] = 500
                data['message'] = repr(e)
            response.data = data
            # response.status_code = 200
        # 最终返回的响应是 response.content 中的内容，如果不赋值一下，可能 content 不对
        response.content = response.rendered_content
        return response

    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        if settings.DEBUG:
            error_logger.error(exception, exc_info=True)  # 如果开启 sentry，这一行代码会将错误事件扔给 sentry
            s = repr(exception)
            data = {'code': 500, 'message': s, 'data': s}
            return None
            # return JsonResponse(data)
        else:
            error_logger.error(exception, exc_info=True)  # 如果开启 sentry，这一行代码会将错误事件扔给 sentry
            s = repr(exception)
            data = {'code': 500, 'message': s, 'data': s}
            return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
