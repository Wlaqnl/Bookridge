from django.db import models
from django.conf import settings
# Create your models here.

class LibraryLocation(models.Model):
    loc_code = models.IntegerField(default=0)
    city = models.CharField(max_length=45)
    gu = models.CharField(max_length=45)
    location_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='location_libraries', blank=True)

class Library(models.Model):
    lib_code = models.IntegerField(default=0)
    lib_name = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    tel = models.CharField(max_length=45)
    fax = models.CharField(max_length=45)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    homepage = models.CharField(max_length=45)
    closed = models.CharField(max_length=45)
    operating_time = models.CharField(max_length=45)
    book_count = models.IntegerField(default=0)
    library_location = models.ForeignKey(LibraryLocation, on_delete=models.CASCADE)