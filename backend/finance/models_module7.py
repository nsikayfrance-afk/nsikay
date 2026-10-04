from django.db import models


class WalletSecurityCheck(models.Model):
    wallet_id = models.IntegerField()
    action = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50,
        default="pending"
    )
    risk_level = models.CharField(
        max_length=50,
        default="low"
    )
    details = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.action} - {self.status}"


class FinancialComplianceLog(models.Model):
    operation = models.CharField(
        max_length=100
    )
    user_id = models.IntegerField()
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )
    currency = models.CharField(
        max_length=10
    )
    result = models.CharField(
        max_length=50,
        default="approved"
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.operation


class FraudDetectionAlert(models.Model):
    wallet_id = models.IntegerField()
    alert_type = models.CharField(
        max_length=100
    )
    severity = models.CharField(
        max_length=50,
        default="medium"
    )
    description = models.TextField()
    resolved = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.alert_type


class ComplianceReport(models.Model):
    title = models.CharField(
        max_length=255
    )
    period = models.CharField(
        max_length=100
    )
    total_operations = models.IntegerField(
        default=0
    )
    suspicious_operations = models.IntegerField(
        default=0
    )
    status = models.CharField(
        max_length=50,
        default="generated"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
