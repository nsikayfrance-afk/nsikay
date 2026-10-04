from rest_framework import viewsets
from .models import (
    MediaContent,
    TVChannel,
    TVProgram,
    Event,
    EventRegistration
)
from .serializers import (
    MediaContentSerializer,
    TVChannelSerializer,
    TVProgramSerializer,
    EventSerializer,
    EventRegistrationSerializer
)


class MediaContentViewSet(viewsets.ModelViewSet):
    queryset = MediaContent.objects.all()
    serializer_class = MediaContentSerializer


class TVChannelViewSet(viewsets.ModelViewSet):
    queryset = TVChannel.objects.all()
    serializer_class = TVChannelSerializer


class TVProgramViewSet(viewsets.ModelViewSet):
    queryset = TVProgram.objects.all()
    serializer_class = TVProgramSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

