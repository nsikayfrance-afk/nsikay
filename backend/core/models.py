from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    USER_TYPES = (
        ("private", "Profil privé"),
        ("professional", "Profil professionnel"),
        ("company", "Entreprise"),
        ("artist", "Artiste"),
        ("member", "Membre association"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_type = models.CharField(
        max_length=50,
        choices=USER_TYPES
    )

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    social_links = models.JSONField(
        default=dict
    )

    verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username

