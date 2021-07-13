from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    genre = models.TextField(null=True, blank=True)
    genre_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_genres', blank=True)

class Hobby(models.Model):
    hobby = models.TextField(null=True, blank=True)
    hobby_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_hobbies', blank=True)

class SearchLog(models.Model):
    search = models.TextField(null=True, blank=True)
    count = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
