from django.db import models


class CountryServiceStatus(models.Model):
    country_code = models.CharField(max_length=3)
    country_name = models.CharField(max_length=100)

    # Normalisation ISO NSIKAY
    iso2_code = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        db_index=True,
    )

    iso_numeric_code = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        db_index=True,
    )

    # Plusieurs lignes historiques peuvent representer
    # le meme pays ISO3.
    is_primary = models.BooleanField(
        default=False,
        db_index=True,
    )

    # Statut operationnel NSIKAY.
    # Il sera defini ulterieurement par l'administration.
    is_operational = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        unique_together = ("country_code", "country_name")
        indexes = [
            models.Index(
                fields=["country_code", "is_primary"]
            ),
            models.Index(
                fields=["country_code", "is_operational"]
            ),
        ]

    def __str__(self):
        return self.country_name


class GlobalService(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)

    active_global = models.BooleanField(default=False)

    countries = models.ManyToManyField(
        CountryServiceStatus,
        through="ServiceActivation",
        blank=True
    )

    def __str__(self):
        return self.name


class ServiceActivation(models.Model):
    service = models.ForeignKey(
        GlobalService,
        on_delete=models.CASCADE
    )

    country = models.ForeignKey(
        CountryServiceStatus,
        on_delete=models.CASCADE
    )

    active = models.BooleanField(default=False)

    reason = models.TextField(
        blank=True,
        null=True
    )

    validated_by_admin = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.service} - {self.country}"

class ServiceRule(models.Model):
    service = models.OneToOneField(
        GlobalService,
        on_delete=models.CASCADE,
        related_name="rule"
    )

    certification_required = models.BooleanField(default=True)

    partner_bank_required = models.BooleanField(default=False)

    health_insurance_required = models.BooleanField(default=False)

    remote_activation_allowed = models.BooleanField(default=True)

    admin_validation_required = models.BooleanField(default=True)

    country_authorization_required = models.BooleanField(default=True)

    financial_partner_required = models.BooleanField(default=False)

    active_by_default = models.BooleanField(default=False)

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Regles - {self.service.name}"


