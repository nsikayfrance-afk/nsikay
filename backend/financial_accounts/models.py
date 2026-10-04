from decimal import Decimal

from django.db import models


class FinancialAccount(models.Model):

    class AccountType(models.TextChoices):
        PRINCIPAL = "PRINCIPAL", "Compte principal"
        GIFTS = "GIFTS", "Compte cadeaux"
        FEES = "FEES", "Compte commissions et frais"
        PAYOUT = "PAYOUT", "Compte retraits"

    class AccountStatus(models.TextChoices):
        PLANNED = "PLANNED", "Planifie"
        ACTIVE = "ACTIVE", "Actif"
        SUSPENDED = "SUSPENDED", "Suspendu"
        CLOSED = "CLOSED", "Ferme"

    code = models.CharField(
        max_length=80,
        unique=True,
        db_index=True
    )

    name = models.CharField(max_length=150)

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        db_index=True
    )

    currency = models.CharField(
        max_length=3,
        db_index=True
    )

    status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.PLANNED,
        db_index=True
    )

    bank_partner = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    external_reference = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    current_balance = models.DecimalField(
        max_digits=24,
        decimal_places=2,
        default=Decimal("0.00")
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    is_internal_ledger = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["account_type", "currency", "code"]
        indexes = [
            models.Index(fields=["account_type", "currency"]),
            models.Index(fields=["status", "currency"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class BankReconciliation(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        MATCHED = "MATCHED", "Rapproche"
        DIFFERENCE = "DIFFERENCE", "Difference"
        CANCELLED = "CANCELLED", "Annule"

    reference = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    financial_account = models.ForeignKey(
        FinancialAccount,
        on_delete=models.PROTECT,
        related_name="reconciliations"
    )

    nsikay_reference = models.CharField(
        max_length=150,
        db_index=True
    )

    bank_reference = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    transaction_type = models.CharField(
        max_length=80
    )

    currency = models.CharField(
        max_length=3
    )

    nsikay_amount = models.DecimalField(
        max_digits=24,
        decimal_places=2
    )

    bank_amount = models.DecimalField(
        max_digits=24,
        decimal_places=2,
        null=True,
        blank=True
    )

    difference = models.DecimalField(
        max_digits=24,
        decimal_places=2,
        default=Decimal("0.00")
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    transaction_date = models.DateTimeField()

    notes = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-transaction_date"]
        indexes = [
            models.Index(fields=["status", "currency"]),
            models.Index(fields=["nsikay_reference"]),
            models.Index(fields=["bank_reference"]),
        ]

    def __str__(self):
        return self.reference


class GiftFinancialLedger(models.Model):

    class OperationType(models.TextChoices):
        PURCHASE = "PURCHASE", "Achat de cadeaux"
        SEND = "SEND", "Envoi de cadeaux"
        RECEIVE = "RECEIVE", "Reception de cadeaux"
        WITHDRAWAL = "WITHDRAWAL", "Retrait"
        REFUND = "REFUND", "Remboursement"
        ADJUSTMENT = "ADJUSTMENT", "Ajustement"

    reference = models.CharField(
        max_length=120,
        unique=True,
        db_index=True
    )

    operation_type = models.CharField(
        max_length=20,
        choices=OperationType.choices
    )

    currency = models.CharField(
        max_length=3
    )

    amount = models.DecimalField(
        max_digits=24,
        decimal_places=2
    )

    buyer_reference = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    sender_reference = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    beneficiary_reference = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    financial_account = models.ForeignKey(
        FinancialAccount,
        on_delete=models.PROTECT,
        related_name="gift_ledger_entries"
    )

    related_reference = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["operation_type", "currency"]),
            models.Index(fields=["buyer_reference"]),
            models.Index(fields=["beneficiary_reference"]),
        ]

    def __str__(self):
        return self.reference
