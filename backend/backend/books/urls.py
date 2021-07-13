from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path('get_book_list/', views.get_book_list, name="get_book_list"),
    path('get_pop_book_list/', views.get_pop_book_list, name="get_pop_book_list"),
    path('book_detail/<int:book_pk>/', views.book_detail, name="book_detail"),
    path('book_search/<int:page_num>/', views.book_search, name="book_search"),
    path('like/', views.like_book, name='like_book'),
]