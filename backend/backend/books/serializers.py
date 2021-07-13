from rest_framework import serializers
from .models import Book
from .models import PopularBook

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class PopularBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularBook
        fields = '__all__'