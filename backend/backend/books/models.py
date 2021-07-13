from django.db import models
from django.conf import settings

# Create your models here.
class Kdc(models.Model):
    num = models.CharField(max_length=45)
    desc = models.TextField(null=True, blank=True)

class IsbnAdd1(models.Model):
    num = models.CharField(max_length=45)
    target = models.CharField(max_length=45)
    desc = models.TextField(null=True, blank=True)

class IsbnAdd2(models.Model):
    num = models.CharField(max_length=45)
    shape = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)

class IsbnAdd3(models.Model):
    num = models.CharField(max_length=45)
    desc = models.TextField(null=True, blank=True)

class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500, null=True, blank=True)
    publisher = models.CharField(max_length=500, null=True, blank=True)
    vol = models.CharField(max_length=100, null=True, blank=True)
    pub_date = models.CharField(max_length=100, null=True, blank=True)
    isbn = models.CharField(max_length=100)
    price = models.CharField(max_length=100, null=True, blank=True)
    img_url = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    isbn_add1 = models.ForeignKey(IsbnAdd1, on_delete=models.CASCADE, default=None)
    isbn_add2 = models.ForeignKey(IsbnAdd2, on_delete=models.CASCADE, default=None)
    isbn_add3 = models.ForeignKey(IsbnAdd3, on_delete=models.CASCADE, default=None)
    kdc = models.ForeignKey(Kdc, on_delete=models.CASCADE, null=True, blank=True)

class PopularBook(models.Model):
    gender = models.IntegerField(default=0)
    age = models.CharField(max_length=45)
    ranking = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    rent_count = models.IntegerField(default=0)
    location = models.TextField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)

class BookRequest(models.Model):
    isbn = models.CharField(max_length=45)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Hashtag(models.Model):
    hashtag = models.TextField()
    hashtag_books = models.ManyToManyField(Book, related_name='book_hashtags', blank=True)





