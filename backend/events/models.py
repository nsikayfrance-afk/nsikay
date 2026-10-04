from django.conf import settings
from django.db import models


class Event(models.Model):

    STATUS_DRAFT = "DRAFT"
    STATUS_PENDING = "PENDING"
    STATUS_PUBLISHED = "PUBLISHED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_FINISHED = "FINISHED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Brouillon"),
        (STATUS_PENDING, "En attente de validation"),
        (STATUS_PUBLISHED, "Publié"),
        (STATUS_CANCELLED, "Annulé"),
        (STATUS_FINISHED, "Terminé"),
    ]

    MODE_PHYSICAL = "PHYSICAL"
    MODE_ONLINE = "ONLINE"
    MODE_HYBRID = "HYBRID"

    MODE_CHOICES = [
        (MODE_PHYSICAL, "Présentiel"),
        (MODE_ONLINE, "En ligne"),
        (MODE_HYBRID, "Hybride"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True)

    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=120, blank=True, default="")

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nsikay_events",
    )

    country = models.CharField(max_length=120, blank=True, default="")
    city = models.CharField(max_length=120, blank=True, default="")
    venue = models.CharField(max_length=255, blank=True, default="")
    address = models.CharField(max_length=500, blank=True, default="")

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    mode = models.CharField(
        max_length=20,
        choices=MODE_CHOICES,
        default=MODE_PHYSICAL,
    )

    online_url = models.URLField(blank=True, default="")

    is_free = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)

    poster = models.ImageField(
        upload_to="events/posters/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_at", "-created_at"]

    def __str__(self):
        return self.title


class EventTicket(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True, default="")

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=10,
        default="EUR",
    )

    quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["price", "id"]

    def __str__(self):
        return f"{self.event.title} - {self.name}"


class EventRegistration(models.Model):

    STATUS_PENDING = "PENDING"
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente"),
        (STATUS_CONFIRMED, "Confirmée"),
        (STATUS_CANCELLED, "Annulée"),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_registrations",
    )

    ticket = models.ForeignKey(
        EventTicket,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registrations",
    )

    quantity = models.PositiveIntegerField(default=1)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event.title} - {self.user}"


class EventMediaLink(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="media_links",
    )

    media_asset_id = models.PositiveBigIntegerField()

    role = models.CharField(
        max_length=50,
        default="PROGRAM",
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "media_asset_id")

    def __str__(self):
        return f"{self.event.title} - media {self.media_asset_id}"
