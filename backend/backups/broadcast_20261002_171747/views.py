from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(
        detail=True,
        methods=["post"],
        url_path="publish",
    )
    def publish(self, request, pk=None):

        stream = self.get_object()

        channel_id = request.data.get("channel_id")

        if not channel_id:
            return Response(
                {
                    "success": False,
                    "error": "channel_id est obligatoire.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        from api_nsikay.tv.models import TVChannel

        channel = get_object_or_404(
            TVChannel,
            pk=channel_id,
        )

        if not stream.stream_url:
            return Response(
                {
                    "success": False,
                    "error": "Le LiveStream ne possède aucune stream_url.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        channel.video_url = stream.stream_url
        channel.is_live = True
        channel.is_active = True
        channel.save(
            update_fields=[
                "video_url",
                "is_live",
                "is_active",
            ]
        )

        return Response(
            {
                "success": True,
                "message": "LiveStream publié sur la chaîne TV.",
                "stream": {
                    "id": stream.id,
                    "title": stream.title,
                    "stream_url": stream.stream_url,
                },
                "channel": {
                    "id": channel.id,
                    "title": channel.title,
                    "category": channel.category,
                    "video_url": channel.video_url,
                    "is_live": channel.is_live,
                    "is_active": channel.is_active,
                },
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="unpublish",
    )
    def unpublish(self, request, pk=None):

        stream = self.get_object()

        from api_nsikay.tv.models import TVChannel

        channels = TVChannel.objects.filter(
            video_url=stream.stream_url
        )

        count = channels.update(
            is_live=False
        )

        return Response(
            {
                "success": True,
                "message": "Diffusion arrêtée sur les chaînes utilisant ce flux.",
                "stream_id": stream.id,
                "channels_updated": count,
            },
            status=status.HTTP_200_OK,
        )


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
