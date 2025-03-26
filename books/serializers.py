from rest_framework import serializers
from .models import Book, BookCopy, BookLending
from authors.serializers import AuthorShortSerializer
from genres.serializers import GenreShortSerializer


class BookSerializer(serializers.ModelSerializer):
    copies_available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genre', 'isbn', 'published_date', 'desc', 'page_count', 'lang', 'copies_available']

    def get_copies_available(self, obj):
        return obj.book_copies.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['authors'] = AuthorShortSerializer(instance.authors).data
        data['genre'] = GenreShortSerializer(instance.genre).data
        return data


class AuthorBookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    isbn = serializers.CharField(read_only=True)
    published_date = serializers.DateField(read_only=True)
    copies_available = serializers.IntegerField(read_only=True)


class BookShortSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    isbn = serializers.CharField(read_only=True)


class BookCopySerializer(serializers.ModelSerializer):
    current_lending = serializers.SerializerMethodField()


    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'inventory_number', 'condition', 'is_available', 'added_time', 'current_lending']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['book'] = BookShortSerializer(instance.book).data
        return data

class BookCopyShortSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    inventory_number = serializers.CharField(read_only=True)



class BookLendingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookLending
        fields = ['id', 'book_copy', 'borrower_name', 'borrower_email', 'borrowed_date', 'due_date', 'returned_date', 'status']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['book_copy'] = BookCopyShortSerializer(instance.book_copy).data
        return data