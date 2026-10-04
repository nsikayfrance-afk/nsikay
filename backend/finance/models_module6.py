from django.db import models
from decimal import Decimal


class FinancialRoutingRule(models.Model):

    name = models.CharField(max_length=255)

    country = models.CharField(
        max_length=10,
        default="GLOBAL"
    )

    currency = models.CharField(
        max_length=10,
        default="EUR"
    )

    destination = models.CharField(
        max_length=255
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("100.00")
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name



class FinancialControlReport(models.Model):

    report_type = models.CharField(
        max_length=100
    )

    country = models.CharField(
        max_length=10,
        default="GLOBAL"
    )

    currency = models.CharField(
        max_length=10,
        default="EUR"
    )

    total_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
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
        return self.report_type



class NSIKAYRevenueFlow(models.Model):

    SOURCE_TYPES = (
        ("wenze","WENZE"),
        ("gift","Cadeaux"),
        ("ticket","Billetterie"),
        ("advertising","Publicité"),
        ("transfer","Transfert"),
        ("commission","Commission"),
    )


    source = models.CharField(
        max_length=50,
        choices=SOURCE_TYPES
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="EUR"
    )

    country = models.CharField(
        max_length=10,
        default="GLOBAL"
    )

    routed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.source}-{self.amount}"



class FinancialAuditLog(models.Model):

    action = models.CharField(
        max_length=255
    )

    user_id = models.IntegerField(
        null=True,
        blank=True
    )

    details = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.action
