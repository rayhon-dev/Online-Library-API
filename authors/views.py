from rest_framework import generics
from .models import Author
from .pagination import AuthorPagination, AuthorBookPagination
from .serializers import AuthorSerializer
from books.serializers import AuthorBookSerializer
from books.models import Book


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = AuthorPagination



class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'pk'


class AuthorBookView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorBookSerializer
    pagination_class = AuthorBookPagination

    def get_queryset(self):
        return Book.objects.filter(authors__id=self.kwargs['pk'])