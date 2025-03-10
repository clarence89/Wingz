from rest_framework.pagination import LimitOffsetPagination

class ViewsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'