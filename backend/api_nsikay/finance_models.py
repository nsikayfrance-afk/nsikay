from django.db import models
from django.conf import settings


class FinanceRule(models.Model):

    name = models.CharField(
        max_length=100
    )


    max_daily_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=10000
    )


    currency = models.CharField(
        max_length=10,
        default="USD"
    )


    active = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



class FinanceApproval(models.Model):

    STATUS = [

        ("PENDING","PENDING"),

        ("APPROVED","APPROVED"),

        ("REJECTED","REJECTED"),

    ]


    reference = models.CharField(
        max_length=120,
        unique=True
    )


    operation = models.CharField(
        max_length=100
    )


    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )


    currency = models.CharField(
        max_length=10
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="PENDING"
    )


    approved_by = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        null=True,

        blank=True,

        on_delete=models.SET_NULL

    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



class FinancialMonitoring(models.Model):


    transaction_reference = models.CharField(
        max_length=120
    )


    risk_level = models.CharField(
        max_length=30,
        default="LOW"
    )


    message = models.TextField(
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


