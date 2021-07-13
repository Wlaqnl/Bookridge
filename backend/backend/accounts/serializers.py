from rest_framework import serializers
from .models import User, UserPrivacy, Calendar


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','birth','name', 'address', 'latitude', 'longitude', 'gender', 'social', 'social_id')


class UserPrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPrivacy
        fields = ('birth', 'name', 'address', 'gender', 'calendar', 'favorite', 'review')


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = '__all__'
        read_only_fields = ('id')
