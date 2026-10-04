from django.conf import settings
from django.db import models


class CameraSystem(models.Model):
    CAMERA_TYPES = [
        ("IP", "Camera IP"),
        ("RTMP", "Source RTMP"),
        ("HDMI", "HDMI Capture"),
        ("SDI", "SDI Broadcast"),
        ("WEBRTC", "WebRTC Live"),
    ]

    name = models.CharField(max_length=150)
    source_type = models.CharField(
        max_length=20,
        choices=CAMERA_TYPES,
        default="IP"
    )

    source_url = models.URLField(blank=True)

    resolution = models.CharField(
        max_length=50,
        default="4K"
    )

    frame_rate = models.IntegerField(
        default=60
    )

    is_live = models.BooleanField(
        default=False
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name



class LiveStream(models.Model):
    title = models.CharField(max_length=200)

    camera = models.ForeignKey(
        CameraSystem,
        on_delete=models.CASCADE
    )

    stream_url = models.URLField()

    quality = models.CharField(
        max_length=50,
        default="4K Ultra HD"
    )

    recording_enabled = models.BooleanField(
        default=True
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title



class VideoEffect(models.Model):
    name = models.CharField(max_length=150)

    effect_type = models.CharField(
        max_length=100
    )

    parameters = models.JSONField(
        default=dict
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name



class TextAnimation(models.Model):
    title = models.CharField(max_length=150)

    text = models.TextField()

    animation_type = models.CharField(
        max_length=100,
        default="fade"
    )

    position = models.CharField(
        max_length=50,
        default="bottom"
    )

    duration = models.IntegerField(
        default=5
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title



class AudioControl(models.Model):
    name = models.CharField(max_length=150)

    volume = models.IntegerField(
        default=100
    )

    audio_effect = models.CharField(
        max_length=100,
        blank=True
    )

    muted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name



class RegieScene(models.Model):
    name = models.CharField(
        max_length=150
    )

    cameras = models.ManyToManyField(
        CameraSystem,
        blank=True
    )

    effects = models.ManyToManyField(
        VideoEffect,
        blank=True
    )

    texts = models.ManyToManyField(
        TextAnimation,
        blank=True
    )

    audio = models.ManyToManyField(
        AudioControl,
        blank=True
    )

    active = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name



class BroadcastSchedule(models.Model):
    title = models.CharField(
        max_length=200
    )

    scene = models.ForeignKey(
        RegieScene,
        on_delete=models.SET_NULL,
        null=True
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    live = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.title


# ============================================================
# NSIKAY BROADCAST CENTRAL
# ============================================================

class Broadcast(models.Model):

    STATUS_DRAFT = "DRAFT"
    STATUS_READY = "READY"
    STATUS_LIVE = "LIVE"
    STATUS_STOPPED = "STOPPED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Brouillon"),
        (STATUS_READY, "Prêt"),
        (STATUS_LIVE, "En direct"),
        (STATUS_STOPPED, "Arrêté"),
    ]

    title = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )

    source_stream = models.ForeignKey(
        "tv_regie.LiveStream",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="broadcasts"
    )

    source_url = models.URLField(
        blank=True,
        default=""
    )

    thumbnail = models.URLField(
        blank=True,
        default=""
    )

    destinations = models.JSONField(
        default=list,
        blank=True
    )

    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nsikay_broadcasts"
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    stopped_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} [{self.status}]"


