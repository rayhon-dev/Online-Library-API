from django.contrib import admin
from .models import Book, BookCopy, BookLending

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'isbn', 'page_count', 'lang')
    search_fields = ('title', 'isbn', 'lang')
    list_filter = ('published_date', 'lang', 'genre')
    filter_horizontal = ('authors',)


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('book', 'inventory_number', 'condition', 'is_available', 'added_time')
    search_fields = ('inventory_number',)
    list_filter = ('condition', 'is_available')


@admin.register(BookLending)
class BookLendingAdmin(admin.ModelAdmin):
    list_display = ('borrower_name', 'book_copy', 'borrowed_date', 'due_date', 'returned_date', 'status')
    search_fields = ('borrower_name', 'borrower_email')
    list_filter = ('status', 'due_date')
