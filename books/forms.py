from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Review, UserProfile


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'cover_image', 'published_year', 'isbn']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'A brief description of the book...'}),
            'published_year': forms.NumberInput(attrs={'placeholder': 'e.g. 1984'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'ISBN (optional)'}),
        }


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-radio'}),
    )

    class Meta:
        model = Review
        fields = ['rating', 'title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Summarize your review'}),
            'body': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Share your thoughts about this book...'}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Your email address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'favorite_genre', 'website', 'reading_goal']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell the community about yourself...'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com'}),
            'reading_goal': forms.NumberInput(attrs={'placeholder': 'e.g. 24'}),
        }


class BookSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search books, authors...'}),
        label='',
    )
    genre = forms.ChoiceField(
        required=False,
        choices=[('', 'All Genres')] + Book._meta.get_field('genre').choices,
        label='',
    )
