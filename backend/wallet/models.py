from django.db import models
from django.conf import settings


class Wallet(models.Model):

    STATUS = [
        ("ACTIVE","ACTIVE"),
        ("BLOCKED","BLOCKED"),
        ("SUSPENDED","SUSPENDED"),
        ("CLOSED","CLOSED"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='wallet_related_items', on_delete=models.CASCADE
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
        return f"Wallet {self.user}"


class WalletBalance(models.Model):

    wallet = models.ForeignKey(
        Wallet,
        related_name='balances', on_delete=models.CASCADE
    )

    currency = models.CharField(
        max_length=10
    )

    available_balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    locked_balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        unique_together = (
            "wallet",
            "currency"
        )


class WalletTransaction(models.Model):

    TYPES = [
        ("DEPOSIT","DEPOSIT"),
        ("WITHDRAWAL","WITHDRAWAL"),
        ("TRANSFER","TRANSFER"),
        ("PAYMENT","PAYMENT"),
        ("REFUND","REFUND"),
        ("FEE","FEE"),
    ]


    wallet = models.ForeignKey(
        Wallet,
        related_name='wallet_transactions', on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=TYPES
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    status = models.CharField(
        max_length=30,
        default="PENDING"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class ExchangeRate(models.Model):

    base_currency = models.CharField(
        max_length=10
    )

    target_currency = models.CharField(
        max_length=10
    )

    rate = models.DecimalField(
        max_digits=20,
        decimal_places=6
    )

    source = models.CharField(
        max_length=100,
        default="NSIKAY"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class WalletSecurityEvent(models.Model):

    wallet = models.ForeignKey(
        Wallet,
        related_name='security_events', on_delete=models.CASCADE
    )

    event = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )






from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class WalletOperation(models.Model):

    TYPES = (
        ("deposit","DEPOT"),
        ("withdraw","RETRAIT"),
        ("transfer","TRANSFERT"),
    )

    wallet = models.ForeignKey(
        "wallet.Wallet",
        on_delete=models.CASCADE,
        related_name="operations"
    )

    operation_type = models.CharField(
        max_length=20,
        choices=TYPES
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="USD"
    )

    fee = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    destination_wallet = models.ForeignKey(
        "wallet.Wallet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="incoming_operations"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.operation_type} {self.amount} {self.currency}"



class WalletCommission(models.Model):

    transfer_fee_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.25
    )

    withdrawal_fee_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.20
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

from django.db import models


class WalletAuditLog(models.Model):

    ACTIONS = (
        ("LOGIN","Connexion"),
        ("DEPOSIT","Dépôt"),
        ("WITHDRAW","Retrait"),
        ("TRANSFER","Transfert"),
        ("SECURITY","Sécurité"),
    )


    wallet = models.ForeignKey(
        "wallet.Wallet",
        on_delete=models.CASCADE,
        related_name="audit_logs"
    )


    action = models.CharField(
        max_length=30,
        choices=ACTIONS
    )


    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )


    details = models.JSONField(
        default=dict
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.action} - {self.wallet}"

from django.db import models


class WalletKYCProfile(models.Model):

    LEVELS = (
        ("LEVEL_1","Niveau 1"),
        ("LEVEL_2","Niveau 2"),
        ("LEVEL_3","Niveau 3"),
    )


    user = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="wallet_kyc"
    )


    level = models.CharField(
        max_length=20,
        choices=LEVELS,
        default="LEVEL_1"
    )


    daily_deposit_limit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=1000
    )


    daily_withdraw_limit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=500
    )


    daily_transfer_limit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=500
    )


    active = models.BooleanField(
        default=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )



    def __str__(self):

        return f"{self.user} - {self.level}"

from django.db import models


class WalletBankAccount(models.Model):

    STATUS = (

        ("PENDING","En attente"),

        ("VERIFIED","Certifié"),

        ("BLOCKED","Bloqué"),

    )


    wallet = models.ForeignKey(

        "wallet.Wallet",

        on_delete=models.CASCADE,

        related_name="bank_accounts"

    )


    bank_name = models.CharField(

        max_length=255

    )


    account_name = models.CharField(

        max_length=255

    )


    account_number = models.CharField(

        max_length=100

    )


    country = models.CharField(

        max_length=100

    )


    currency = models.CharField(

        max_length=10,

        default="USD"

    )


    status = models.CharField(

        max_length=20,

        choices=STATUS,

        default="PENDING"

    )


    certified = models.BooleanField(

        default=False

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    def __str__(self):

        return self.bank_name + " - " + self.account_name


