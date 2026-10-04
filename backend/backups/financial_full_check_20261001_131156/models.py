from django.db import models
from django.contrib.auth.models import User



class PartnerApplication(models.Model):

    STATUS = [

        ("pending","En attente"),

        ("certification","Certification"),

        ("approved","Certifié"),

        ("rejected","Refusé"),

    ]


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="partner_finance_relation"
    )


    business_name = models.CharField(
        max_length=200
    )


    phone = models.CharField(
        max_length=50
    )


    address = models.TextField()


    social_links = models.TextField(
        blank=True
    )


    documents = models.TextField(
        blank=True
    )


    status = models.CharField(
        max_length=50,
        choices=STATUS,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



class PartnerCertification(models.Model):

    partner = models.OneToOneField(
        PartnerApplication,
        on_delete=models.CASCADE,
        related_name="partner_certification_relation"
    )


    identity_verified = models.BooleanField(
        default=False
    )


    documents_verified = models.BooleanField(
        default=False
    )


    certified_by = models.CharField(
        max_length=200,
        blank=True
    )


    certification_date = models.DateTimeField(
        auto_now_add=True
    )



class PartnerSupply(models.Model):

    partner = models.ForeignKey(
        PartnerApplication,
        on_delete=models.CASCADE,
        related_name="partner_supply_relation"
    )


    bank = models.ForeignKey(
        "banking.Bank",
        on_delete=models.PROTECT
    )


    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT
    )


    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )


    status = models.CharField(
        max_length=50,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



class PartnerWallet(models.Model):

    partner = models.ForeignKey(
        PartnerApplication,
        on_delete=models.CASCADE,
        related_name="partner_wallet_relation"
    )


    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT
    )


    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )
from django.db import models


class PartnerDeposit(models.Model):

    STATUS = [

        ("pending","En attente"),

        ("verified","Vérifié"),

        ("approved","Approuvé"),

        ("rejected","Refusé"),

    ]


    partner = models.ForeignKey(
        "partner_finance.PartnerWallet",
        on_delete=models.CASCADE,
        related_name="partner_deposit_relation"
    )


    bank = models.ForeignKey(
        "banking.Bank",
        on_delete=models.CASCADE,
        related_name="bank_partner_deposit_relation"
    )


    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )


    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT
    )


    reference = models.CharField(
        max_length=100,
        unique=True
    )


    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



class SupplyTransaction(models.Model):

    partner = models.ForeignKey(
        "partner_finance.PartnerWallet",
        on_delete=models.CASCADE,
        related_name="supply_transaction_relation"
    )


    deposit = models.OneToOneField(
        PartnerDeposit,
        on_delete=models.CASCADE,
        related_name="deposit_supply_transaction_relation"
    )


    amount_added = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )


    approved_by_bank = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )




