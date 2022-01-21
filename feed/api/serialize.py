from rest_framework import serializers
from models import Note
class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            'id',
            'body',
            'total_likes'
        )