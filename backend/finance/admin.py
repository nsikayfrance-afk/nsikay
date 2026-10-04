from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import FinancialOperation, FeeConfiguration


@admin.register(FinancialOperation)
class FinancialOperationAdmin(admin.ModelAdmin):

    list_display = (
        "operation_type",
        "amount",
        "currency",
        "fee",
        "status",
        "created_at",
    )

    search_fields = (
        "reference",
    )


@admin.register(FeeConfiguration)
class FeeConfigurationAdmin(admin.ModelAdmin):

    list_display = (
        "operation",
        "percentage",
        "active",
    )
from django.contrib import admin

from .models import (
    PartnerBankAccount,
    BankRoutingOperation
)



@admin.register(PartnerBankAccount)
class PartnerBankAccountAdmin(admin.ModelAdmin):

    list_display = (
        "bank_name",
        "country",
        "currency",
        "balance",
        "active",
    )



@admin.register(BankRoutingOperation)
class BankRoutingOperationAdmin(admin.ModelAdmin):

    list_display = (
        "operation_type",
        "amount",
        "country",
        "currency",
        "created_at",
    )
