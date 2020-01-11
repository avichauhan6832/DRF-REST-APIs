from rest_framework import serializers
from .models import Event


class EventSerializers(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = 'id', 'title', 'author', 'event_date', 'limit'
        # fields = '__all__'


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)
