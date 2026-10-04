from rest_framework import serializers
from .models import (
    MediaContent,
    TVChannel,
    TVProgram,
    Event,
    EventRegistration
)


class MediaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = '__all__'


class TVChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVChannel
        fields = '__all__'


class TVProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVProgram
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = '__all__'

