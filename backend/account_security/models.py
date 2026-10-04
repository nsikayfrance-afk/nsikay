from django.conf import settings
from django.db import models
from django.utils import timezone


class PasswordRecoveryRequest(models.Model):
    CHANNEL_EMAIL = "email"

    CHANNEL_CHOICES = (
        (CHANNEL_EMAIL, "E-mail"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_recovery_requests",
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES,
        default=CHANNEL_EMAIL,
    )

    destination = models.CharField(
        max_length=320,
        blank=True,
    )

    code_hash = models.CharField(
        max_length=128,
    )

    expires_at = models.DateTimeField()

    attempts = models.PositiveSmallIntegerField(
        default=0,
    )

    max_attempts = models.PositiveSmallIntegerField(
        default=5,
    )

    used = models.BooleanField(
        default=False,
    )

    requested_ip_hash = models.CharField(
        max_length=128,
        blank=True,
    )

    user_agent_hash = models.CharField(
        max_length=128,
        blank=True,
    )

    requested_at = models.DateTimeField(
        auto_now_add=True,
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-requested_at"]
        indexes = [
            models.Index(
                fields=["user", "-requested_at"],
                name="pwdrec_user_requested_idx",
            ),
            models.Index(
                fields=["expires_at", "used"],
                name="pwdrec_expiry_used_idx",
            ),
        ]

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def is_exhausted(self):
        return self.attempts >= self.max_attempts

    def is_usable(self):
        return (
            not self.used
            and not self.is_expired()
            and not self.is_exhausted()
        )

    def __str__(self):
        return f"Password recovery #{self.pk} - user={self.user_id}"
