from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Book, Review, UserProfile, ReadingList
from .forms import BookForm, ReviewForm, UserRegisterForm, UserProfileForm, BookSearchForm


# ── Signals (inline to keep single-file) ────────────────────────────────────
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


# ── Home ─────────────────────────────────────────────────────────────────────
def home(request):
    recent_books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    ).order_by('-created_at')[:8]

    top_books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    ).filter(num_reviews__gte=1).order_by('-avg_rating')[:4]

    recent_reviews = Review.objects.select_related('book', 'user').order_by('-created_at')[:5]

    stats = {
        'books': Book.objects.count(),
        'reviews': Review.objects.count(),
        'members': User.objects.count(),
    }

    return render(request, 'books/home.html', {
        'recent_books': recent_books,
        'top_books': top_books,
        'recent_reviews': recent_reviews,
        'stats': stats,
    })


# ── Books ─────────────────────────────────────────────────────────────────────
def book_list(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    )

    if form.is_valid():
        q = form.cleaned_data.get('q')
        genre = form.cleaned_data.get('genre')
        if q:
            books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))
        if genre:
            books = books.filter(genre=genre)

    sort = request.GET.get('sort', 'newest')
    if sort == 'rating':
        books = books.order_by('-avg_rating')
    elif sort == 'reviews':
        books = books.order_by('-num_reviews')
    elif sort == 'title':
        books = books.order_by('title')
    else:
        books = books.order_by('-created_at')

    return render(request, 'books/book_list.html', {
        'books': books,
        'form': form,
        'sort': sort,
        'total': books.count(),
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.select_related('user').all()
    user_review = None
    reading_status = None

    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        entry = ReadingList.objects.filter(user=request.user, book=book).first()
        reading_status = entry.status if entry else None

    review_form = ReviewForm(instance=user_review) if request.user.is_authenticated else None

    rating_breakdown = {}
    for i in range(1, 6):
        count = reviews.filter(rating=i).count()
        rating_breakdown[i] = {
            'count': count,
            'pct': round(count / reviews.count() * 100) if reviews.count() else 0,
        }

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'user_review': user_review,
        'review_form': review_form,
        'rating_breakdown': rating_breakdown,
        'reading_status': reading_status,
    })


@login_required
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            messages.success(request, f'"{book.title}" has been added successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Add'})


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.added_by != request.user and not request.user.is_staff:
        messages.error(request, "You can only edit books you added.")
        return redirect('book_detail', pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Edit', 'book': book})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.added_by != request.user and not request.user.is_staff:
        messages.error(request, "You can only delete books you added.")
        return redirect('book_detail', pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted.')
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


# ── Reviews ───────────────────────────────────────────────────────────────────
@login_required
def review_submit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    existing = Review.objects.filter(book=book, user=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been saved!')
            return redirect('book_detail', pk=pk)
    return redirect('book_detail', pk=pk)


@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user and not request.user.is_staff:
        messages.error(request, "You can only delete your own reviews.")
        return redirect('book_detail', pk=review.book.pk)
    book_pk = review.book.pk
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('book_detail', pk=book_pk)


@login_required
@require_POST
def review_like(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user in review.likes.all():
        review.likes.remove(request.user)
        liked = False
    else:
        review.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': review.like_count})


# ── Reading List ──────────────────────────────────────────────────────────────
@login_required
@require_POST
def reading_list_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    status = request.POST.get('status')
    if status == 'remove':
        ReadingList.objects.filter(user=request.user, book=book).delete()
        messages.success(request, f'Removed "{book.title}" from your reading list.')
    elif status in ['want', 'reading', 'read']:
        entry, _ = ReadingList.objects.get_or_create(user=request.user, book=book)
        entry.status = status
        entry.save()
        label = dict(ReadingList.STATUS_CHOICES)[status]
        messages.success(request, f'Marked "{book.title}" as "{label}".')
    return redirect('book_detail', pk=pk)


# ── Auth ──────────────────────────────────────────────────────────────────────
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Folio, {user.username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# ── User Profile ──────────────────────────────────────────────────────────────
def profile(request, username):
    target_user = get_object_or_404(User, username=username)
    profile_obj, _ = UserProfile.objects.get_or_create(user=target_user)
    reviews = target_user.reviews.select_related('book').order_by('-created_at')
    reading_list = target_user.reading_list.select_related('book').order_by('-added_at')

    reading_by_status = {
        'want': reading_list.filter(status='want'),
        'reading': reading_list.filter(status='reading'),
        'read': reading_list.filter(status='read'),
    }

    return render(request, 'books/profile.html', {
        'target_user': target_user,
        'profile': profile_obj,
        'reviews': reviews,
        'reading_by_status': reading_by_status,
    })


@login_required
def profile_edit(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile_obj)
    return render(request, 'books/profile_edit.html', {'form': form})


# ── Community ─────────────────────────────────────────────────────────────────
def community(request):
    members = User.objects.annotate(
        review_count=Count('reviews')
    ).order_by('-review_count')[:12]

    recent_reviews = Review.objects.select_related('book', 'user').order_by('-created_at')[:10]

    return render(request, 'books/community.html', {
        'members': members,
        'recent_reviews': recent_reviews,
    })
