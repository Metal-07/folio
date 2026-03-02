from django.contrib import admin
from .models import Book, Review, UserProfile, ReadingList


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'average_rating', 'review_count', 'added_by', 'created_at']
    list_filter = ['genre', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'title', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'title']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_genre', 'reading_goal', 'books_read']
    search_fields = ['user__username']


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'status', 'added_at']
    list_filter = ['status']
