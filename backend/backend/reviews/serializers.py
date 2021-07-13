from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Review, Phrase, ReviewComment

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'hitcount', 'created_at', 'updated_at')


class PhraseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phrase
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = '__all__'