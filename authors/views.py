from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from books.serializers import BookSerializer
from .models import Author
from .serializers import AuthorSerializer


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer



class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'pk'


class AuthorBookView(APIView):
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        books = author.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=200)

