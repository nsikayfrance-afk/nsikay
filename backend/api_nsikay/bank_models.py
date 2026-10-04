from django.db import models
from wallet.models import Wallet


class PartnerBank(models.Model):

    STATUS = [

        ("ACTIVE","ACTIVE"),
        ("BLOCKED","BLOCKED"),

    ]


    name = models.CharField(
        max_length=150
    )


    country = models.CharField(
        max_length=100
    )


    swift_code = models.CharField(
        max_length=50,
        blank=True
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="ACTIVE"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.name



class SettlementAccount(models.Model):

    bank = models.ForeignKey(
        PartnerBank,
        on_delete=models.CASCADE
    )


    currency = models.CharField(
        max_length=10
    )


    account_reference = models.CharField(
        max_length=100
    )


    active = models.BooleanField(
        default=True
    )



class BankDeposit(models.Model):

    STATUS = [

        ("PENDING","PENDING"),

        ("APPROVED","APPROVED"),

        ("REJECTED","REJECTED"),

    ]


    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE
    )


    bank = models.ForeignKey(
        PartnerBank,
        on_delete=models.CASCADE
    )


    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )


    currency = models.CharField(
        max_length=10
    )


    reference = models.CharField(
        max_length=120,
        unique=True
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="PENDING"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

