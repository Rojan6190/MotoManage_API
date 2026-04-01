from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'   #allows ?page_size=20 and by default also allow ?page=20
    max_page_size = 100