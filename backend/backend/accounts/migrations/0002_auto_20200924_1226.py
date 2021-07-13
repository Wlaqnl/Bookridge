# Generated by Django 3.1.1 on 2020-09-24 03:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_books',
            field=models.ManyToManyField(related_name='like_users', to='books.Book'),
        ),
        migrations.AddField(
            model_name='user',
            name='unlike_books',
            field=models.ManyToManyField(related_name='unlike_users', to='books.Book'),
        ),
    ]
