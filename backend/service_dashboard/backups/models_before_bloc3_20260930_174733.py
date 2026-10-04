from django.db import models


class OperationalCountryConfigurationLog(models.Model):
    admin_user = models.CharField(max_length=150)
    selected_count = models.PositiveIntegerField()
    selected_codes = models.TextField()
    action = models.CharField(
        max_length=50,
        default="configuration_240_pays"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    rolled_back = models.BooleanField(default=False)
    rolled_back_at = models.DateTimeField(
        blank=True,
        null=True
    )
    rolled_back_by = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    rollback_reason = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["admin_user"]),
            models.Index(fields=["rolled_back"]),
        ]

    def __str__(self):
        return (
            f"{self.action} - "
            f"{self.selected_count} pays - "
            f"{self.admin_user}"
        )


class OperationalCountryConfigurationSnapshot(models.Model):
    configuration_log = models.OneToOneField(
        OperationalCountryConfigurationLog,
        on_delete=models.CASCADE,
        related_name="snapshot",
    )

    previous_operational_codes = models.TextField(
        blank=True,
        default=""
    )

    previous_operational_count = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Snapshot #{self.id} - "
            f"{self.previous_operational_count} pays"
        )

class ServiceDashboardLog(models.Model):
    ACTION_CHOICES = [
        ("activate", "Activation"),
        ("disable", "Désactivation"),
        ("validation", "Validation"),
        ("rejection", "Refus"),
    ]

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
    )
    admin_user = models.CharField(
        max_length=150,
        blank=True,
    )
    comment = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    country = models.ForeignKey(
        "service_control.CountryServiceStatus",
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        "service_control.GlobalService",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.action} - {self.service} - {self.country}"
