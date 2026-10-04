from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=10,
        unique=True
    )

    symbol = models.CharField(
        max_length=10
    )

    reference_nsikay = models.BooleanField(
        default=False
    )

    approved = models.BooleanField(
        default=False
    )


    def __str__(self):
        return self.code



class Wallet(models.Model):

    user = models.ForeignKey(
        User,
        related_name='finance_wallets', on_delete=models.CASCADE
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT
    )

    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class WalletTransaction(models.Model):

    TYPES = (
        ("deposit","DÃ©pÃ´t"),
        ("withdraw","Retrait"),
        ("transfer","Transfert"),
        ("purchase","Achat"),
        ("reward","RÃ©compense"),
    )

    wallet = models.ForeignKey(
        Wallet,
        related_name='finance_wallets', on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=50,
        choices=TYPES
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    reference = models.CharField(
        max_length=255,
        unique=True
    )

    status = models.CharField(
        max_length=50,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class ExchangeRate(models.Model):

    from_currency = models.ForeignKey(
        Currency,
        related_name='exchange_from', on_delete=models.CASCADE
    )

    to_currency = models.ForeignKey(
        Currency,
        related_name='exchange_to', on_delete=models.CASCADE
    )

    rate = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

    source = models.CharField(
        max_length=255
    )

    active_date = models.DateTimeField(
        auto_now_add=True
    )



from django.db import models



class FinancialLedger(models.Model):

    TYPES = (

        ("DEPOSIT","DÃ©pÃ´t"),

        ("WITHDRAW","Retrait"),

        ("TRANSFER","Transfert"),

        ("FEE","Frais"),

        ("EXCHANGE","Change"),

    )


    wallet = models.ForeignKey(

        "wallet.Wallet",

        on_delete=models.CASCADE,

        related_name="ledger_entries"

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

        max_length=255,

        unique=True

    )


    metadata = models.JSONField(

        default=dict

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    def __str__(self):

        return self.reference



class ExchangeRateHistory(models.Model):


    from_currency = models.CharField(

        max_length=10

    )


    to_currency = models.CharField(

        max_length=10

    )


    rate = models.DecimalField(

        max_digits=20,

        decimal_places=8

    )


    source = models.CharField(

        max_length=255

    )


    effective_date = models.DateTimeField(

        auto_now_add=True

    )

from django.db import models



class MerchantPayment(models.Model):


    STATUS = (

        ("PENDING","En attente"),

        ("PAID","PayÃ©"),

        ("FAILED","Ã‰chec"),

    )


    wallet = models.ForeignKey(

        "wallet.Wallet",

        on_delete=models.CASCADE,

        related_name="merchant_payments"

    )


    merchant_name = models.CharField(

        max_length=255

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


    reference = models.CharField(

        max_length=255,

        unique=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )




class BankReconciliation(models.Model):


    STATUS = (

        ("OPEN","Ouvert"),

        ("MATCHED","RapprochÃ©"),

        ("REVIEW","ContrÃ´le"),

    )


    bank_account = models.ForeignKey(

        "wallet.WalletBankAccount",

        on_delete=models.CASCADE,

        related_name="reconciliations"

    )


    amount = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )


    currency = models.CharField(

        max_length=10

    )


    bank_reference = models.CharField(

        max_length=255

    )


    status = models.CharField(

        max_length=20,

        choices=STATUS,

        default="OPEN"

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class PlatformCommission(models.Model):


    wallet = models.ForeignKey(

        "wallet.Wallet",

        on_delete=models.CASCADE,

        related_name="platform_commissions"

    )


    amount = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )


    currency = models.CharField(

        max_length=10

    )


    reason = models.CharField(

        max_length=255

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )

from django.db import models



class AuditLog(models.Model):


    ACTIONS = (

        ("LOGIN","Connexion"),

        ("TRANSACTION","Transaction"),

        ("BLOCK","Blocage"),

        ("ADMIN","Action administrateur"),

        ("KYC","ContrÃ´le KYC"),

    )


    user = models.ForeignKey(

        "auth.User",

        null=True,

        blank=True,

        on_delete=models.SET_NULL,

        related_name="audit_logs"

    )


    action = models.CharField(

        max_length=50,

        choices=ACTIONS

    )


    description = models.TextField()


    ip_address = models.GenericIPAddressField(

        null=True,

        blank=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class WalletSecurityStatus(models.Model):


    STATUS = (

        ("ACTIVE","Actif"),

        ("BLOCKED","BloquÃ©"),

        ("REVIEW","ContrÃ´le"),

    )


    wallet = models.OneToOneField(

        "wallet.Wallet",

        on_delete=models.CASCADE,

        related_name="security_status"

    )


    status = models.CharField(

        max_length=20,

        choices=STATUS,

        default="ACTIVE"

    )


    reason = models.TextField(

        blank=True

    )


    updated_at = models.DateTimeField(

        auto_now=True

    )



class FraudDetectionEvent(models.Model):


    wallet = models.ForeignKey(

        "wallet.Wallet",

        on_delete=models.CASCADE,

        related_name="fraud_events"

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


    risk_score = models.IntegerField(

        default=0

    )


    blocked = models.BooleanField(

        default=False

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )

from django.db import models



class KYCCompliance(models.Model):


    user = models.OneToOneField(

        "auth.User",

        on_delete=models.CASCADE,

        related_name="kyc_compliance"

    )


    identity_verified = models.BooleanField(

        default=False

    )


    documents_verified = models.BooleanField(

        default=False

    )


    approved = models.BooleanField(

        default=False

    )


    checked_at = models.DateTimeField(

        auto_now=True

    )


    def is_compliant(self):

        return (

            self.identity_verified

            and

            self.documents_verified

            and

            self.approved

        )

from django.db import models



class SellerProfile(models.Model):


    user = models.OneToOneField(

        "auth.User",

        on_delete=models.CASCADE,

        related_name="seller_profile"

    )


    company_name = models.CharField(

        max_length=255

    )


    certified = models.BooleanField(

        default=False

    )


    active = models.BooleanField(

        default=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class MarketplaceProduct(models.Model):


    seller = models.ForeignKey(

        SellerProfile,

        on_delete=models.CASCADE,

        related_name="products"

    )


    name = models.CharField(

        max_length=255

    )


    description = models.TextField(

        blank=True

    )


    price = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )


    currency = models.CharField(

        max_length=10,

        default="USD"

    )


    available = models.BooleanField(

        default=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class MarketplaceOrder(models.Model):


    STATUS = (

        ("PENDING","En attente"),

        ("PAID","PayÃ©e"),

        ("DELIVERED","LivrÃ©e"),

        ("CANCELLED","AnnulÃ©e"),

    )


    buyer = models.ForeignKey(

        "auth.User",

        on_delete=models.CASCADE,

        related_name="market_orders"

    )


    product = models.ForeignKey(

        MarketplaceProduct,

        on_delete=models.CASCADE

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


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class MarketplaceCommission(models.Model):


    order = models.OneToOneField(

        MarketplaceOrder,

        on_delete=models.CASCADE,

        related_name="commission"

    )


    rate = models.DecimalField(

        max_digits=5,

        decimal_places=4,

        default=0.0000

    )


    amount = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class FinancialOperation(models.Model):

    TYPES = (
        ("transfer", "Transfert"),
        ("deposit", "DÃ©pÃ´t"),
        ("withdraw", "Retrait"),
        ("mobile_money", "Mobile Money"),
        ("wenze", "WENZE"),
        ("commission", "Commission"),
        ("gift", "Cadeau"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    operation_type = models.CharField(
        max_length=50,
        choices=TYPES
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    fee = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    currency = models.CharField(
        max_length=10,
        default="EUR"
    )

    reference = models.CharField(
        max_length=255,
        unique=True
    )

    status = models.CharField(
        max_length=50,
        default="completed"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.operation_type} - {self.amount} {self.currency}"


class FeeConfiguration(models.Model):

    operation = models.CharField(
        max_length=50,
        unique=True
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=3
    )

    active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return self.operation
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FinancialOperation(models.Model):

    TYPES = (
        ("transfer", "Transfert"),
        ("deposit", "Depot"),
        ("withdraw", "Retrait"),
        ("mobile_money", "Mobile Money"),
        ("wenze", "WENZE"),
        ("commission", "Commission"),
        ("gift", "Cadeau"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    operation_type = models.CharField(
        max_length=50,
        choices=TYPES
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    fee = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    currency = models.CharField(
        max_length=10,
        default="EUR"
    )

    reference = models.CharField(
        max_length=255,
        unique=True
    )

    status = models.CharField(
        max_length=50,
        default="completed"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class FeeConfiguration(models.Model):

    operation = models.CharField(
        max_length=50,
        unique=True
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=3
    )

    active = models.BooleanField(
        default=True
    )
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PartnerBankAccount(models.Model):

    bank_name = models.CharField(
        max_length=255
    )

    country = models.CharField(
        max_length=100
    )

    currency = models.CharField(
        max_length=10,
        default="EUR"
    )

    account_reference = models.CharField(
        max_length=255,
        unique=True
    )

    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return self.bank_name



class BankRoutingOperation(models.Model):

    TYPES = (
        ("commission","Commission"),
        ("card","Carte"),
        ("wenze","WENZE"),
        ("advertising","PublicitÃ©"),
        ("event","Ã‰vÃ©nement"),
    )


    bank_account = models.ForeignKey(
        PartnerBankAccount,
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


    country = models.CharField(
        max_length=100
    )


    currency = models.CharField(
        max_length=10
    )


    reference = models.CharField(
        max_length=255,
        unique=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )
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
from django.db import models



class WalletSecurityCheck(models.Model):
    wallet = models.ForeignKey(
        "Wallet",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        default="pending"
    )

    details = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class FinancialComplianceLog(models.Model):
    action = models.CharField(
        max_length=255
    )

    details = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class FraudDetectionAlert(models.Model):
    reference = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    severity = models.CharField(
        max_length=50,
        default="medium"
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class ComplianceReport(models.Model):
    title = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=50,
        default="pending"
    )

    details = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

