from django.conf import settings
from django.db import models


class NsikayProfile(models.Model):

    PROFILE_TYPES = [
        ("person", "Personne"),
        ("professional", "Professionnel / Métier"),
        ("company", "Entreprise"),
        ("bank", "Banque"),
        ("school", "École / Université"),
        ("training", "Centre de formation"),
        ("health", "Hôpital / Santé"),
        ("association", "Association / ONG"),
        ("institution", "Institution"),
        ("artist", "Artiste / Créateur"),
        ("agent", "Agent / Expert"),
    ]

    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("private", "Privé"),
    ]

    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("active", "Actif"),
        ("suspended", "Suspendu"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="nsikay_profiles",
    )

    profile_type = models.CharField(
        max_length=30,
        choices=PROFILE_TYPES,
    )

    display_name = models.CharField(
        max_length=200,
    )

    legal_name = models.CharField(
        max_length=250,
        blank=True,
    )

    professional_title = models.CharField(
        max_length=200,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    sector = models.CharField(
        max_length=150,
        blank=True,
    )

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="public",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    is_primary = models.BooleanField(
        default=False,
    )

    certification_required = models.BooleanField(
        default=False,
    )

    certification_status = models.CharField(
        max_length=30,
        default="not_required",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-is_primary", "-updated_at"]
        indexes = [
            models.Index(fields=["user", "profile_type"]),
            models.Index(fields=["profile_type", "status"]),
            models.Index(fields=["country", "profile_type"]),
        ]

    def __str__(self):
        return f"{self.display_name} — {self.get_profile_type_display()}"
