
from django.db import models
from django.conf import settings


class SecurityIncident(models.Model):
    """
    Incident sécurité NSIKAY
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    incident_type = models.CharField(
        max_length=100
    )

    description = models.TextField()

    severity = models.CharField(
        max_length=50,
        default="normal"
    )

    status = models.CharField(
        max_length=50,
        default="open"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class ComplianceValidation(models.Model):
    """
    Validation conformité financière
    """

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    operation = models.CharField(
        max_length=150
    )

    country = models.CharField(
        max_length=5
    )

    currency = models.CharField(
        max_length=5
    )

    approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class FraudMonitoring(models.Model):
    """
    Surveillance anti fraude NSIKAY
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    action = models.CharField(
        max_length=150
    )

    risk_level = models.CharField(
        max_length=50,
        default="low"
    )

    detected = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class FinancialSecurityReport(models.Model):
    """
    Rapport sécurité financière
    """

    title = models.CharField(
        max_length=150
    )

    country = models.CharField(
        max_length=5
    )

    currency = models.CharField(
        max_length=5
    )

    summary = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

