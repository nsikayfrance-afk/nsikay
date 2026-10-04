from django.contrib import admin

from .models import (
    BankReconciliation,
    FinancialAccount,
    GiftFinancialLedger,
)


@admin.register(FinancialAccount)
class FinancialAccountAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "account_type",
        "currency",
        "status",
        "current_balance",
        "bank_partner",
        "is_internal_ledger",
    )

    list_filter = (
        "account_type",
        "currency",
        "status",
        "is_internal_ledger",
    )

    search_fields = (
        "code",
        "name",
        "bank_partner",
        "external_reference",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(BankReconciliation)
class BankReconciliationAdmin(admin.ModelAdmin):

    list_display = (
        "reference",
        "financial_account",
        "transaction_type",
        "currency",
        "nsikay_amount",
        "bank_amount",
        "difference",
        "status",
        "transaction_date",
    )

    list_filter = (
        "status",
        "currency",
        "transaction_type",
    )

    search_fields = (
        "reference",
        "nsikay_reference",
        "bank_reference",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(GiftFinancialLedger)
class GiftFinancialLedgerAdmin(admin.ModelAdmin):

    list_display = (
        "reference",
        "operation_type",
        "currency",
        "amount",
        "buyer_reference",
        "beneficiary_reference",
        "financial_account",
        "created_at",
    )

    list_filter = (
        "operation_type",
        "currency",
    )

    search_fields = (
        "reference",
        "buyer_reference",
        "sender_reference",
        "beneficiary_reference",
        "related_reference",
    )

    readonly_fields = (
        "created_at",
    )
