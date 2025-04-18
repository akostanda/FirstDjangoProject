from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'date', 'description', 'location', 'organizer', 'participant']
        read_only_fields = ['organizer']

