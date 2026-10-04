from rest_framework import serializers

from .models import (Broadcast
    CameraSystem,
    LiveStream,
    VideoEffect,
    TextAnimation,
    AudioControl,
    RegieScene,
    BroadcastSchedule,
)



class CameraSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraSystem
        fields = "__all__"



class LiveStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStream
        fields = "__all__"



class VideoEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoEffect
        fields = "__all__"



class TextAnimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextAnimation
        fields = "__all__"



class AudioControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioControl
        fields = "__all__"



class RegieSceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegieScene
        fields = "__all__"



class BroadcastScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BroadcastSchedule
        fields = "__all__"


# ============================================================
# NSIKAY BROADCAST SERIALIZER
# ============================================================

class BroadcastSerializer(serializers.ModelSerializer):

    operator_username = serializers.CharField(
        source="operator.username",
        read_only=True
    )

    class Meta:
        model = Broadcast
        fields = "__all__"
        read_only_fields = [
            "operator",
            "started_at",
            "stopped_at",
            "created_at",
            "updated_at",
            "operator_username",
        ]



