from django.db import models


class Activity(models.Model):
    TYPE_CHOICES = [
        ("professional", "Professionnel"),
        ("company", "Entreprise"),
        ("bank", "Banque"),
        ("service", "Service"),
        ("shop", "Commerce"),
        ("creator", "Créateur"),
        ("artist", "Artiste"),
        ("sport", "Sport"),
        ("training", "Formation"),
        ("school", "École"),
        ("health", "Santé"),
        ("association", "Association"),
        ("institution", "Institution"),
        ("agent", "Agent / Expert"),
        ("media", "Média"),
        ("agriculture", "Agriculture"),
        ("technology", "Technologie"),
        ("gift_reseller", "Revendeur de cadeaux"),
        ("logistics", "Logistique"),
        ("other", "Autre"),
    ]

    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("active", "Active"),
        ("suspended", "Suspendue"),
    ]

    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("private", "Privé"),
    ]

    CERTIFICATION_CHOICES = [
        ("not_required", "Non requise"),
        ("pending", "En attente"),
        ("certified", "Certifiée"),
        ("rejected", "Refusée"),
        ("expired", "Expirée"),
    ]

    profile = models.ForeignKey(
        "nsikay_profiles.NsikayProfile",
        on_delete=models.CASCADE,
        related_name="activities",
    )

    source_profile = models.OneToOneField(
        "nsikay_profiles.NsikayProfile",
        on_delete=models.PROTECT,
        related_name="migrated_activity",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=200)
    activity_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default="other",
    )

    description = models.TextField(blank=True)
    sector = models.CharField(max_length=150, blank=True)

    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="public",
    )

    certification_required = models.BooleanField(default=False)

    certification_status = models.CharField(
        max_length=20,
        choices=CERTIFICATION_CHOICES,
        default="not_required",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["profile", "activity_type"]),
            models.Index(fields=["activity_type", "status"]),
            models.Index(fields=["country", "city"]),
        ]

    def __str__(self):
        return self.name


class Service(models.Model):
    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("active", "Actif"),
        ("suspended", "Suspendu"),
    ]

    CERTIFICATION_CHOICES = [
        ("not_required", "Non requise"),
        ("pending", "En attente"),
        ("certified", "Certifié"),
        ("rejected", "Refusé"),
        ("expired", "Expiré"),
    ]

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="services",
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=150, blank=True)

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
    )

    currency = models.CharField(
        max_length=10,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    certification_required = models.BooleanField(default=False)

    certification_status = models.CharField(
        max_length=20,
        choices=CERTIFICATION_CHOICES,
        default="not_required",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planifié"),
        ("active", "Actif"),
        ("completed", "Terminé"),
        ("suspended", "Suspendu"),
    ]

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planned",
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

