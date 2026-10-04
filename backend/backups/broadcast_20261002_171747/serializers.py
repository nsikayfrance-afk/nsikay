from rest_framework import serializers

from .models import (
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

