from django.conf import settings
from django.db import models


class FinancialRoutingRule(models.Model):

    SOURCE_TYPES = (
        ("WENZE", "WENZE"),
        ("EVENT", "Événement"),
        ("TICKET", "Billetterie"),
        ("ADVERTISING", "Publicité"),
        ("MEMBERSHIP", "Adhésion"),
        ("GIFT", "Cadeau"),
        ("COMMISSION", "Commission"),
        ("CREDIT", "Crédit"),
        ("INVESTMENT", "Investissement"),
        ("OTHER", "Autre"),
    )

    OPERATION_TYPES = (
        ("REVENUE", "Revenu"),
        ("TRANSFER", "Transfert"),
        ("WITHDRAWAL", "Retrait"),
        ("DEPOSIT", "Dépôt"),
        ("SETTLEMENT", "Règlement"),
    )

    PARTNER_TYPES = (
        ("BANK", "Banque"),
        ("MOBILE_MONEY", "Mobile Money"),
        ("VISA", "Visa"),
        ("FINANCIAL_PARTNER", "Partenaire financier"),
        ("INTERNAL", "NSIKAY interne"),
    )

    STATUS_CHOICES = (
        ("DRAFT", "Brouillon"),
        ("PENDING", "En attente de validation"),
        ("APPROVED", "Approuvé"),
        ("SUSPENDED", "Suspendu"),
        ("REJECTED", "Rejeté"),
    )

    country_code = models.CharField(
        max_length=10,
        blank=True,
        default="",
        help_text="Code ISO du pays. Vide = règle internationale."
    )

    country_name = models.CharField(
        max_length=120,
        blank=True,
        default=""
    )

    currency_code = models.CharField(
        max_length=10,
        blank=True,
        default="",
        help_text="EUR, USD, CDF ou autre devise approuvée."
    )

    source_type = models.CharField(
        max_length=30,
        choices=SOURCE_TYPES
    )

    source_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Nom précis de la source de revenu."
    )

    operation_type = models.CharField(
        max_length=30,
        choices=OPERATION_TYPES,
        default="REVENUE"
    )

    partner_type = models.CharField(
        max_length=30,
        choices=PARTNER_TYPES,
        default="BANK"
    )

    partner_name = models.CharField(
        max_length=255,
        help_text="Banque ou partenaire financier destinataire."
    )

    bank_name = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    bank_country = models.CharField(
        max_length=120,
        blank=True,
        default=""
    )

    bank_account_reference = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Référence interne du compte. Ne pas stocker de données bancaires sensibles non nécessaires."
    )

    destination_label = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    priority = models.PositiveIntegerField(
        default=100,
        help_text="Plus le nombre est petit, plus la règle est prioritaire."
    )

    active = models.BooleanField(
        default=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="DRAFT"
    )

    valid_from = models.DateTimeField(
        null=True,
        blank=True
    )

    valid_until = models.DateTimeField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True,
        default=""
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="financial_routing_rules_created"
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="financial_routing_rules_approved"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["priority", "-created_at"]
        indexes = [
            models.Index(fields=["country_code", "currency_code"]),
            models.Index(fields=["source_type", "active"]),
            models.Index(fields=["status", "active"]),
            models.Index(fields=["partner_type", "partner_name"]),
        ]

    def __str__(self):
        country = self.country_code or "INTERNATIONAL"
        currency = self.currency_code or "TOUTES_DEVISES"
        return f"{self.source_type} - {country} - {currency} - {self.partner_name}"


class FinancialRoutingLog(models.Model):

    ACTIONS = (
        ("CREATED", "Créée"),
        ("UPDATED", "Modifiée"),
        ("APPROVED", "Approuvée"),
        ("SUSPENDED", "Suspendue"),
        ("ACTIVATED", "Activée"),
        ("DEACTIVATED", "Désactivée"),
    )

    rule = models.ForeignKey(
        FinancialRoutingRule,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    action = models.CharField(
        max_length=30,
        choices=ACTIONS
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    details = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]


class FinancialFeeRule(models.Model):

    TRANSFER_INTERNAL = "TRANSFER_INTERNAL"
    TRANSFER_EXTERNAL = "TRANSFER_EXTERNAL"
    WITHDRAWAL = "WITHDRAWAL"
    WENZE = "WENZE"

    FEE_TYPES = (
        (TRANSFER_INTERNAL, "Transfert interne NSIKAY"),
        (TRANSFER_EXTERNAL, "Transfert externe"),
        (WITHDRAWAL, "Retrait"),
        (WENZE, "Vente WENZE"),
    )

    fee_type = models.CharField(
        max_length=40,
        choices=FEE_TYPES,
        unique=True
    )

    percentage = models.DecimalField(
        max_digits=6,
        decimal_places=3
    )

    active = models.BooleanField(
        default=True
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.fee_type} = {self.percentage}%"
