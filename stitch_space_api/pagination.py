from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlparse, parse_qs

class PageNumberOnlyPagination(PageNumberPagination):
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