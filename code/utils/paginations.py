from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            ('results', data),
            ('page', self.page.number),
            ('maximum_page', self.page.paginator.num_pages),
            ('page_size', self.get_page_size(self.request)),
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'page': {
                    'type': 'integer',
                    'example': 2,
                },
                'maximum_page': {
                    'type': 'integer',
                    'example': 7,
                },
                'page_size': {
                    'type': 'integer',
                    'example': 20,
                },
                'results': schema,
            },
        }


def build_number_pagination(build_max_page_size: int = 50):
    class NumberPagination(DefaultPageNumberPagination):
        max_page_size = build_max_page_size

    return NumberPagination
