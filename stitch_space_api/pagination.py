from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlparse, parse_qs


class PageNumberOnlyPagination(PageNumberPagination):
    """
    Custom pagination class that extends PageNumberPagination.
    Allows clients to set page size via the 'page_size' query parameter,
    with a maximum limit of 1000. Returns a paginated response including
    the total count, next and previous page numbers, and the results.
    """
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        def get_page_number(url):
            if url:
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                return query_params.get('page', [None])[0]
            return None

        return Response({
            'count': self.page.paginator.count,
            'nextPage': get_page_number(self.get_next_link()),
            'previousPage': get_page_number(self.get_previous_link()),
            'results': data
        })
