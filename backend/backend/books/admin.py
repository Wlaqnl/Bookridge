from django.contrib import admin
from .models import Book, PopularBook, BookRequest
# Register your models here.

admin.site.register(Book)
admin.site.register(PopularBook)
admin.site.register(BookRequest)