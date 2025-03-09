from rest_framework import serializers
from .models import Book, BookCopy, BookLending
from authors.serializers import AuthorSerializer
from genres.serializers import GenreSerializer
from authors.models import Author


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    genre = GenreSerializer(read_only=True)

    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True, write_only=True
    )
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genre', 'isbn', 'published_date', 'desc', 'page_count', 'lang', 'author_ids']

    def create(self, validated_data):
        author_ids = validated_data.pop('author_ids', [])
        book = Book.objects.create(**validated_data)
        book.authors.set(author_ids)
        return book

    def update(self, instance, validated_data):
        author_ids = validated_data.pop('author_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if author_ids is not None:
            instance.authors.set(author_ids)

        instance.save()
        return instance


class BookCopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)


    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'inventory_number', 'condition', 'is_available', 'added_time']

class BookLendingSerializer(serializers.ModelSerializer):
    book_copy = BookCopySerializer(read_only=True)
    book_copy_id = serializers.PrimaryKeyRelatedField(
        queryset=BookCopy.objects.all(), write_only=True
    )

    class Meta:
        model = BookLending
        fields = ['id', 'book_copy', 'book_copy_id', 'borrower_name', 'borrower_email', 'borrowed_date', 'due_date', 'returned_date', 'status']

    def create(self, validated_data):
        book_copy = validated_data.pop('book_copy_id')

        # Kitob allaqachon olingan bo'lsa, xatolik qaytariladi
        if not book_copy.is_available:
            raise serializers.ValidationError({"book_copy_id": "This book copy is already borrowed."})

        lending = BookLending.objects.create(book_copy=book_copy, **validated_data)

        # Kitob olingandan keyin uni mavjud emas deb belgilaymiz
        book_copy.is_available = False
        book_copy.save()

        return lending

    def update(self, instance, validated_data):
        returned_date = validated_data.get('returned_date', None)

        # Agar kitob qaytarilgan bo‘lsa, uni "mavjud" qilib belgilaymiz
        if returned_date:
            instance.book_copy.is_available = True
            instance.book_copy.save()

        return super().update(instance, validated_data)