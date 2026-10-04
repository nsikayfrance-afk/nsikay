from rest_framework import viewsets

from .permissions import IsTVRegieOperator

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


class SecureRegieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTVRegieOperator]


class CameraSystemViewSet(SecureRegieViewSet):
    queryset = CameraSystem.objects.all()
    serializer_class = CameraSystemSerializer


class LiveStreamViewSet(SecureRegieViewSet):
    queryset = LiveStream.objects.all()
    serializer_class = LiveStreamSerializer


class VideoEffectViewSet(SecureRegieViewSet):
    queryset = VideoEffect.objects.all()
    serializer_class = VideoEffectSerializer


class TextAnimationViewSet(SecureRegieViewSet):
    queryset = TextAnimation.objects.all()
    serializer_class = TextAnimationSerializer


class AudioControlViewSet(SecureRegieViewSet):
    queryset = AudioControl.objects.all()
    serializer_class = AudioControlSerializer


class RegieSceneViewSet(SecureRegieViewSet):
    queryset = RegieScene.objects.all()
    serializer_class = RegieSceneSerializer


class BroadcastScheduleViewSet(SecureRegieViewSet):
    queryset = BroadcastSchedule.objects.all()
    serializer_class = BroadcastScheduleSerializer

