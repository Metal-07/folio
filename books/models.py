from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


GENRE_CHOICES = [
    ('fiction', 'Fiction'),
    ('non-fiction', 'Non-Fiction'),
    ('mystery', 'Mystery & Thriller'),
    ('sci-fi', 'Science Fiction'),
    ('fantasy', 'Fantasy'),
    ('romance', 'Romance'),
    ('biography', 'Biography'),
    ('history', 'History'),
    ('self-help', 'Self-Help'),
    ('poetry', 'Poetry'),
    ('other', 'Other'),
]


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='fiction')
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    published_year = models.PositiveIntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_books')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.pk])

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def star_display(self):
        avg = self.average_rating
        if avg is None:
            return []
        full = int(avg)
        half = 1 if avg - full >= 0.5 else 0
        empty = 5 - full - half
        return ['full'] * full + ['half'] * half + ['empty'] * empty


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['book', 'user']

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def stars(self):
        return ['full'] * self.rating + ['empty'] * (5 - self.rating)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    favorite_genre = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True)
    website = models.URLField(blank=True)
    reading_goal = models.PositiveIntegerField(default=0, help_text="Books to read this year")

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def books_read(self):
        return self.user.reviews.count()

    @property
    def average_rating_given(self):
        reviews = self.user.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None


class ReadingList(models.Model):
    STATUS_CHOICES = [
        ('want', 'Want to Read'),
        ('reading', 'Currently Reading'),
        ('read', 'Already Read'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_list')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_list_entries')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='want')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"
