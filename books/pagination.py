from rest_framework.pagination import PageNumberPagination


class BookPagination(PageNumberPagination):
    page_size = 10


class BookCopiesPagination(PageNumberPagination):
    page_size = 5


class BookCopyPagination(PageNumberPagination):
    page_size = 10


class BookLendingPagination(PageNumberPagination):
    page_size = 10
