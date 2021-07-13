from django.db import models
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from books.models import Book

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    birth = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    social = models.IntegerField(default=0)
    social_id = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    choice_books = models.ManyToManyField(Book, related_name='choice_users')
    like_books = models.ManyToManyField(Book, related_name='like_users')
    unlike_books = models.ManyToManyField(Book, related_name='unlike_users')
    finish_books = models.ManyToManyField(Book, related_name='finish_users')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class UserPrivacy(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    gender = models.IntegerField(default=0, blank=True)
    name = models.IntegerField(default=0, blank=True)
    address = models.IntegerField(default=0, blank=True)
    birth = models.IntegerField(default=0, blank=True)
    calendar = models.IntegerField(default=0, blank=True)
    favorite = models.IntegerField(default=0, blank=True)
    review = models.IntegerField(default=0, blank=True)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.ManyToManyField(
        User, related_name='to_user', blank=True)
    to_user = models.ManyToManyField(
        User, related_name='from_user', blank=True)


class Calendar(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

