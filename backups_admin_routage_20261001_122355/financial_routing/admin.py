from django.contrib import admin
from .models import (
    FinancialFeeRule,
    FinancialRoutingLog,
    FinancialRoutingRule,
)


@admin.register(FinancialRoutingRule)
class FinancialRoutingRuleAdmin(admin.ModelAdmin):
    list_display = (
        "source_type",
        "country_code",
        "currency_code",
        "partner_type",
        "partner_name",
        "priority",
        "status",
        "active",
    )
    list_filter = (
        "source_type",
        "operation_type",
        "partner_type",
        "status",
        "active",
    )
    search_fields = (
        "country_code",
        "country_name",
        "source_name",
        "partner_name",
        "bank_name",
        "destination_label",
    )
    ordering = ("priority", "-created_at")


@admin.register(FinancialRoutingLog)
class FinancialRoutingLogAdmin(admin.ModelAdmin):
    list_display = (
        "rule",
        "action",
        "performed_by",
        "created_at",
    )
    list_filter = ("action",)
    search_fields = ("rule__partner_name", "rule__source_name")


@admin.register(FinancialFeeRule)
class FinancialFeeRuleAdmin(admin.ModelAdmin):
    list_display = (
        "fee_type",
        "percentage",
        "active",
        "updated_at",
    )
    list_filter = ("fee_type", "active")
