from django.contrib import admin

from .models import (
    CameraSystem,
    LiveStream,
    VideoEffect,
    TextAnimation,
    AudioControl,
    RegieScene,
    BroadcastSchedule,
)


@admin.register(CameraSystem)
class CameraSystemAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("__str__",)


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("__str__",)


@admin.register(VideoEffect)
class VideoEffectAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("__str__",)


@admin.register(TextAnimation)
class TextAnimationAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("__str__",)


@admin.register(AudioControl)
class AudioControlAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("__str__",)


@admin.register(RegieScene)
class RegieSceneAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("__str__",)


@admin.register(BroadcastSchedule)
class BroadcastScheduleAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("__str__",)

