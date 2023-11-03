from rest_framework.pagination import PageNumberPagination


class ListPaginator(PageNumberPagination):
    """ Пагинация для вывода """
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 25
