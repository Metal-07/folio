from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/<int:pk>/review/', views.review_submit, name='review_submit'),
    path('books/<int:pk>/reading-list/', views.reading_list_update, name='reading_list_update'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('review/<int:pk>/like/', views.review_like, name='review_like'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/edit/me/', views.profile_edit, name='profile_edit'),
    path('community/', views.community, name='community'),
]
