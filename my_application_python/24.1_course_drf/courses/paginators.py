from rest_framework.pagination import PageNumberPagination


class CoursePagintor(PageNumberPagination):
    """Пагинатор для курсов"""
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 30


class LessonPagintor(PageNumberPagination):
    """Пагинатор для уроков"""
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 30