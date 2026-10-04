from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class MembershipType(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    contribution_required = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )


    def __str__(self):
        return self.name



class Member(models.Model):

    STATUS = (
        ("pending", "En attente"),
        ("active", "Actif"),
        ("suspended", "Suspendu"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    membership_type = models.ForeignKey(
        MembershipType,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS,
        default="pending"
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )



class Subscription(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="USD"
    )

    payment_status = models.CharField(
        max_length=50,
        default="pending"
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )



class Donation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="USD"
    )

    message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


# ============================================================
# NSIKAY - SYSTEME OFFICIEL D'ADHESION
# ============================================================

class MembershipApplication(models.Model):

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("approved_pending_payment", "Validée - cotisation attendue"),
        ("approved", "Validée"),
        ("refused", "Refusée"),
        ("cancelled", "Annulée"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="nsikay_membership_applications",
    )

    membership_type = models.ForeignKey(
        "MembershipType",
        on_delete=models.PROTECT,
        related_name="applications",
    )

    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True,
    )

    message = models.TextField(
        blank=True,
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_nsikay_membership_applications",
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return f"Demande adhésion #{self.pk} - {self.user}"


class MemberCard(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("suspended", "Suspendue"),
        ("expired", "Expirée"),
        ("cancelled", "Annulée"),
    ]

    member = models.OneToOneField(
        "Member",
        on_delete=models.CASCADE,
        related_name="official_card",
    )

    member_number = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
    )

    qr_token = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        db_index=True,
    )

    issued_at = models.DateTimeField(
        default=timezone.now,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-issued_at"]

    def save(self, *args, **kwargs):

        if not self.member_number:
            year = timezone.now().year

            while True:
                candidate = (
                    f"NSK-{year}-"
                    f"{secrets.token_hex(4).upper()}"
                )

                if not MemberCard.objects.filter(
                    member_number=candidate
                ).exists():
                    self.member_number = candidate
                    break

        if not self.qr_token:
            while True:
                candidate = secrets.token_urlsafe(32)

                if not MemberCard.objects.filter(
                    qr_token=candidate
                ).exists():
                    self.qr_token = candidate
                    break

        super().save(*args, **kwargs)

    @property
    def verification_path(self):
        return f"/association/membership/verify/{self.qr_token}/"

    def __str__(self):
        return self.member_number


class MembershipAuditLog(models.Model):

    ACTION_CHOICES = [
        ("APPLICATION_CREATED", "Demande créée"),
        ("APPROVED", "Demande validée"),
        ("REFUSED", "Demande refusée"),
        ("ACTIVATED", "Adhésion activée"),
        ("CARD_CREATED", "Carte créée"),
        ("CARD_SUSPENDED", "Carte suspendue"),
        ("CARD_REACTIVATED", "Carte réactivée"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nsikay_membership_audit_logs",
    )

    member = models.ForeignKey(
        "Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="membership_audit_logs",
    )

    action = models.CharField(
        max_length=40,
        choices=ACTION_CHOICES,
        db_index=True,
    )

    reference = models.CharField(
        max_length=150,
        blank=True,
    )

    details = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.reference}"



