from django.conf import settings
from django.db import models


class MediaAsset(models.Model):

    TYPE_VIDEO = "VIDEO"
    TYPE_FILM = "FILM"
    TYPE_AUDIO = "AUDIO"
    TYPE_IMAGE = "IMAGE"
    TYPE_PROGRAM = "PROGRAM"
    TYPE_MUSIC = "MUSIC"
    TYPE_JINGLE = "JINGLE"
    TYPE_ADVERTISING = "ADVERTISING"
    TYPE_REPORTAGE = "REPORTAGE"
    TYPE_INTERVIEW = "INTERVIEW"
    TYPE_ARCHIVE = "ARCHIVE"
    TYPE_DOCUMENT = "DOCUMENT"

    TYPE_CHOICES = [
        (TYPE_VIDEO, "Vidéo"),
        (TYPE_FILM, "Film"),
        (TYPE_AUDIO, "Audio"),
        (TYPE_IMAGE, "Image"),
        (TYPE_PROGRAM, "Programme TV"),
        (TYPE_MUSIC, "Musique"),
        (TYPE_JINGLE, "Jingle"),
        (TYPE_ADVERTISING, "Publicité"),
        (TYPE_REPORTAGE, "Reportage"),
        (TYPE_INTERVIEW, "Interview"),
        (TYPE_ARCHIVE, "Archive"),
        (TYPE_DOCUMENT, "Document"),
    ]

    STATUS_DRAFT = "DRAFT"
    STATUS_READY = "READY"
    STATUS_PUBLISHED = "PUBLISHED"
    STATUS_ARCHIVED = "ARCHIVED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Brouillon"),
        (STATUS_READY, "Prêt"),
        (STATUS_PUBLISHED, "Publié"),
        (STATUS_ARCHIVED, "Archivé"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    asset_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default=TYPE_VIDEO
    )

    file = models.FileField(
        upload_to="media_library/assets/",
        blank=True,
        null=True
    )

    thumbnail = models.ImageField(
        upload_to="media_library/thumbnails/",
        blank=True,
        null=True
    )

    original_filename = models.CharField(
        max_length=500,
        blank=True,
        default=""
    )

    mime_type = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="media_library_assets"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class MediaDestination(models.Model):

    KIND_INTERNAL = "INTERNAL"
    KIND_EXTERNAL = "EXTERNAL"

    KIND_CHOICES = [
        (KIND_INTERNAL, "Destination NSIKAY"),
        (KIND_EXTERNAL, "Réseau externe"),
    ]

    TYPE_NSikayTV = "NSIKAY_TV"
    TYPE_ECONOMIE = "ECONOMIE"
    TYPE_SPORT = "SPORT"
    TYPE_CULTURE = "CULTURE"
    TYPE_TECHNOLOGIE = "TECHNOLOGIE"
    TYPE_AGRICULTURE = "AGRICULTURE"
    TYPE_ENVIRONNEMENT = "ENVIRONNEMENT"
    TYPE_SOCIAL = "SOCIAL"
    TYPE_RELIGION = "RELIGION"
    TYPE_ADULT = "ADULT"
    TYPE_EVENEMENTS = "EVENEMENTS"
    TYPE_PUBLICITE = "PUBLICITE"

    TYPE_YOUTUBE = "YOUTUBE"
    TYPE_FACEBOOK = "FACEBOOK"
    TYPE_INSTAGRAM = "INSTAGRAM"
    TYPE_TIKTOK = "TIKTOK"
    TYPE_TWITCH = "TWITCH"
    TYPE_LINKEDIN = "LINKEDIN"
    TYPE_RTMP = "RTMP"
    TYPE_SRT = "SRT"
    TYPE_HLS = "HLS"

    DESTINATION_CHOICES = [
        (TYPE_NSikayTV, "NSIKAY TV"),
        (TYPE_ECONOMIE, "Économie"),
        (TYPE_SPORT, "Sport & Loisirs"),
        (TYPE_CULTURE, "Culture & Art"),
        (TYPE_TECHNOLOGIE, "Technologie & Innovation"),
        (TYPE_AGRICULTURE, "Agriculture & Agronomie"),
        (TYPE_ENVIRONNEMENT, "Environnement"),
        (TYPE_SOCIAL, "Social"),
        (TYPE_RELIGION, "Religion & Histoire"),
        (TYPE_ADULT, "+18"),
        (TYPE_EVENEMENTS, "Événements"),
        (TYPE_PUBLICITE, "Publicité"),
        (TYPE_YOUTUBE, "YouTube"),
        (TYPE_FACEBOOK, "Facebook"),
        (TYPE_INSTAGRAM, "Instagram"),
        (TYPE_TIKTOK, "TikTok"),
        (TYPE_TWITCH, "Twitch"),
        (TYPE_LINKEDIN, "LinkedIn"),
        (TYPE_RTMP, "RTMP personnalisé"),
        (TYPE_SRT, "SRT personnalisé"),
        (TYPE_HLS, "HLS personnalisé"),
    ]

    code = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=150
    )

    destination_type = models.CharField(
        max_length=20,
        choices=KIND_CHOICES,
        default=KIND_INTERNAL
    )

    channel_type = models.CharField(
        max_length=50,
        choices=DESTINATION_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    endpoint_url = models.URLField(
        blank=True,
        default=""
    )

    account_label = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    secret_reference = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["destination_type", "name"]

    def __str__(self):
        return self.name


class MediaDistribution(models.Model):

    STATUS_PENDING = "PENDING"
    STATUS_READY = "READY"
    STATUS_LIVE = "LIVE"
    STATUS_PUBLISHED = "PUBLISHED"
    STATUS_STOPPED = "STOPPED"
    STATUS_FAILED = "FAILED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente"),
        (STATUS_READY, "Prêt"),
        (STATUS_LIVE, "En direct"),
        (STATUS_PUBLISHED, "Publié"),
        (STATUS_STOPPED, "Arrêté"),
        (STATUS_FAILED, "Échec"),
    ]

    asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.CASCADE,
        related_name="distributions"
    )

    destination = models.ForeignKey(
        MediaDestination,
        on_delete=models.CASCADE,
        related_name="distributions"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    external_id = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    message = models.TextField(
        blank=True,
        default=""
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="media_distributions_created"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["asset", "destination"],
                name="unique_media_asset_destination"
            )
        ]

    def __str__(self):
        return f"{self.asset.title} -> {self.destination.name}"


class MediaSegment(models.Model):

    asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.CASCADE,
        related_name="segments"
    )

    title = models.CharField(
        max_length=255
    )

    start_seconds = models.PositiveIntegerField(
        default=0
    )

    end_seconds = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    position = models.PositiveIntegerField(
        default=1
    )

    active = models.BooleanField(
        default=True
    )

    destinations = models.ManyToManyField(
        MediaDestination,
        blank=True,
        related_name="segments"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return f"{self.asset.title} / {self.title}"
