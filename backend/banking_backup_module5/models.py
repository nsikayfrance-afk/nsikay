from django.db import models
from django.contrib.auth.models import User
from finance.models import Wallet, Currency


class Bank(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=255
    )

    country = models.CharField(
        max_length=100
    )

    certified = models.BooleanField(
        default=False
    )

    active = models.BooleanField(
        default=False
    )


class BankAccount(models.Model):

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    account_number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT
    )

    wallet = models.OneToOneField(
        Wallet,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    active = models.BooleanField(
        default=True
    )


class BankingOperation(models.Model):

    TYPES = (
        ("deposit","Dépôt"),
        ("withdraw","Retrait"),
        ("transfer","Transfert"),
        ("payment","Paiement"),
    )

    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE
    )

    operation_type = models.CharField(
        max_length=50,
        choices=TYPES
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=50,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

from django.db import models
from django.contrib.auth.models import User
from finance.models import Currency


class BankCountry(models.Model):

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )

    country = models.CharField(
        max_length=100
    )

    approved = models.BooleanField(
        default=False
    )


class BankCurrency(models.Model):

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT
    )

    approved = models.BooleanField(
        default=False
    )


class BankService(models.Model):

    SERVICE_TYPES = (
        ("account", "Création de compte"),
        ("deposit", "Dépôt"),
        ("withdraw", "Retrait"),
        ("transfer", "Transfert"),
        ("credit", "Crédit"),
        ("insurance", "Assurance"),
        ("exchange", "Change"),
    )

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )

    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPES
    )

    active = models.BooleanField(
        default=False
    )


class BankCredit(models.Model):

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=255
    )

    maximum_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    duration_months = models.IntegerField()

    active = models.BooleanField(
        default=True
    )


class BankInsurance(models.Model):

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=255
    )

    category = models.CharField(
        max_length=100
    )

    active = models.BooleanField(
        default=True
    )


class BankReport(models.Model):

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )
from django.db import models
from django.contrib.auth.models import User
from finance.models import Currency


class AccountOpeningRequest(models.Model):

    STATUS = (
        ("pending", "En attente"),
        ("verification", "Vérification"),
        ("approved", "Accepté"),
        ("rejected", "Refusé"),
        ("activated", "Activé"),
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )

    country = models.CharField(
        max_length=100
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class AccountNumberGenerator(models.Model):

    account = models.OneToOneField(
        "BankAccount",
        on_delete=models.CASCADE
    )

    generated_number = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
from django.db import models
from django.contrib.auth.models import User


class BankUserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="bank_profile"
    )

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=100,
        default="employee"
    )

    active = models.BooleanField(
        default=True
    )
from django.db import models
from django.contrib.auth.models import User


class BankTransaction(models.Model):

    TRANSACTION_TYPES = [

        ("deposit", "Dépôt"),

        ("withdrawal", "Retrait"),

        ("transfer", "Transfert"),

        ("exchange", "Change"),

    ]


    account = models.ForeignKey(
        "BankAccount",
        on_delete=models.CASCADE,
        related_name="transactions"
    )


    transaction_type = models.CharField(
        max_length=50,
        choices=TRANSACTION_TYPES
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
        max_length=50,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


class BankBalance(models.Model):

    account = models.ForeignKey(
        "BankAccount",
        on_delete=models.CASCADE
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


class PartnerApproval(models.Model):

    STATUS = [

        ("pending","En attente"),

        ("accepted","Accepté"),

        ("rejected","Refusé"),

    ]


    partner = models.ForeignKey(
        "partner_finance.PartnerApplication",
        on_delete=models.CASCADE
    )


    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )


    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )


    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT
    )


    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )
from django.db import models


class CashDeposit(models.Model):

    STATUS = [

        ("pending", "En attente"),

        ("verified", "Vérifié"),

        ("approved", "Approuvé"),

        ("rejected", "Refusé"),

    ]


    partner = models.ForeignKey(
        "partner_finance.PartnerApplication",
        on_delete=models.CASCADE
    )


    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )


    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )


    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT
    )


    deposit_reference = models.CharField(
        max_length=100,
        unique=True
    )


    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="pending"
    )


    verified_by = models.CharField(
        max_length=200,
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



class PartnerTransaction(models.Model):

    TYPES = [

        ("withdrawal","Retrait"),

        ("deposit","Dépôt"),

        ("purchase","Achat"),

        ("transfer","Transfert"),

    ]


    partner = models.ForeignKey(
        "partner_finance.PartnerApplication",
        on_delete=models.CASCADE
    )


    transaction_type = models.CharField(
        max_length=50,
        choices=TYPES
    )


    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )


    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT
    )


    commission = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )
from django.db import models


class OnlineBankAccountRequest(models.Model):

    STATUS = [

        ("pending","En attente"),

        ("approved","Approuvé"),

        ("rejected","Refusé"),

        ("active","Actif"),

    ]


    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )


    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )


    country = models.CharField(
        max_length=100
    )


    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT
    )


    account_number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )


    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



class BankCustomerService(models.Model):

    account = models.ForeignKey(
        OnlineBankAccountRequest,
        on_delete=models.CASCADE
    )


    service_name = models.CharField(
        max_length=100
    )


    enabled = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )
from django.db import models


class BankCountryAccess(models.Model):

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )


    country_name = models.CharField(
        max_length=100
    )


    approved = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



class BankCurrencyAccess(models.Model):

    bank = models.ForeignKey(
        "Bank",
        on_delete=models.CASCADE
    )


    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT
    )


    is_official = models.BooleanField(
        default=False
    )


    approved = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

