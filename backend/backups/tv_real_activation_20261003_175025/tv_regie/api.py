from rest_framework import viewsets

from .models import (
    CameraSystem,
    LiveStream,
    VideoEffect,
    TextAnimation,
    AudioControl,
    RegieScene,
    BroadcastSchedule,
)

from .serializers import (
    CameraSystemSerializer,
    LiveStreamSerializer,
    VideoEffectSerializer,
    TextAnimationSerializer,
    AudioControlSerializer,
    RegieSceneSerializer,
    BroadcastScheduleSerializer,
)


class CameraSystemViewSet(viewsets.ModelViewSet):
    queryset = CameraSystem.objects.all()
    serializer_class = CameraSystemSerializer


class LiveStreamViewSet(viewsets.ModelViewSet):
    queryset = LiveStream.objects.all()
    serializer_class = LiveStreamSerializer


class VideoEffectViewSet(viewsets.ModelViewSet):
    queryset = VideoEffect.objects.all()
    serializer_class = VideoEffectSerializer


class TextAnimationViewSet(viewsets.ModelViewSet):
    queryset = TextAnimation.objects.all()
    serializer_class = TextAnimationSerializer


class AudioControlViewSet(viewsets.ModelViewSet):
    queryset = AudioControl.objects.all()
    serializer_class = AudioControlSerializer


class RegieSceneViewSet(viewsets.ModelViewSet):
    queryset = RegieScene.objects.all()
    serializer_class = RegieSceneSerializer


class BroadcastScheduleViewSet(viewsets.ModelViewSet):
    queryset = BroadcastSchedule.objects.all()
    serializer_class = BroadcastScheduleSerializer

