from rest_framework import serializers
from .models import Library
from .models import LibraryLocation

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class LibraryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryLocation
        fields = '__all__'