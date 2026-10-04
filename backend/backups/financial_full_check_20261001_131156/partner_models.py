from django.conf import settings
from django.db import models


class FinancialPartner(models.Model):
    PARTNER_TYPES = [
        ("BANK", "Banque"),
        ("MOBILE_MONEY", "Mobile Money"),
        ("VISA", "Visa"),
        ("FINANCIAL_PARTNER", "Partenaire financier"),
        ("INTERNAL", "Interne NSIKAY"),
    ]

    STATUS_CHOICES = [
        ("DRAFT", "Brouillon"),
        ("PENDING", "En attente"),
        ("APPROVED", "Approuvé"),
        ("SUSPENDED", "Suspendu"),
        ("REJECTED", "Rejeté"),
    ]

    name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=255, blank=True)

    partner_type = models.CharField(
        max_length=30,
        choices=PARTNER_TYPES,
    )

    country_code = models.CharField(
        max_length=10,
        blank=True,
    )

    country_name = models.CharField(
        max_length=120,
        blank=True,
    )

    bank = models.ForeignKey(
        "banking.Bank",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="financial_partner_registry",
    )

    partner_application = models.ForeignKey(
        "partner_finance.PartnerApplication",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="financial_partner_registry",
    )

    external_reference = models.CharField(
        max_length=150,
        blank=True,
    )

    certified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT",
    )

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="financial_partners_created",
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="financial_partners_approved",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["partner_type", "active"]),
            models.Index(fields=["country_code", "active"]),
            models.Index(fields=["status", "active"]),
        ]

    def __str__(self):
        country = self.country_code or "GLOBAL"
        return f"{self.name} - {country}"
