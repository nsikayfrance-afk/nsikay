from django.contrib import admin

from .models import (
    FinancialRoutingRule,
    FinancialRoutingLog,
    FinancialFeeRule,
)


@admin.register(FinancialRoutingRule)
class FinancialRoutingRuleAdmin(admin.ModelAdmin):

    list_display = (
        "country_code",
        "country_name",
        "currency_code",
        "source_type",
        "source_name",
        "operation_type",
        "partner_type",
        "partner_name",
        "destination_label",
        "priority",
        "status",
        "active",
        "valid_from",
        "valid_until",
    )

    list_filter = (
        "country_code",
        "currency_code",
        "source_type",
        "operation_type",
        "partner_type",
        "status",
        "active",
    )

    search_fields = (
        "country_code",
        "country_name",
        "currency_code",
        "source_name",
        "partner_name",
        "bank_name",
        "bank_country",
        "destination_label",
        "bank_account_reference",
    )

    ordering = (
        "country_code",
        "currency_code",
        "source_type",
        "priority",
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "approved_by",
    )

    fieldsets = (
        (
            "1. Périmètre",
            {
                "fields": (
                    "country_code",
                    "country_name",
                    "currency_code",
                )
            },
        ),
        (
            "2. Source financière",
            {
                "fields": (
                    "source_type",
                    "source_name",
                    "operation_type",
                )
            },
        ),
        (
            "3. Partenaire financier",
            {
                "fields": (
                    "partner_type",
                    "partner_name",
                    "bank_name",
                    "bank_country",
                    "bank_account_reference",
                    "destination_label",
                )
            },
        ),
        (
            "4. Routage",
            {
                "fields": (
                    "priority",
                    "active",
                    "status",
                    "valid_from",
                    "valid_until",
                )
            },
        ),
        (
            "5. Gouvernance",
            {
                "fields": (
                    "notes",
                    "created_by",
                    "approved_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

        FinancialRoutingLog.objects.create(
            rule=obj,
            action="UPDATED" if change else "CREATED",
            performed_by=request.user,
            details={
                "admin_action": "change" if change else "create",
                "country_code": obj.country_code,
                "currency_code": obj.currency_code,
                "source_type": obj.source_type,
                "operation_type": obj.operation_type,
                "partner_type": obj.partner_type,
                "partner_name": obj.partner_name,
                "destination_label": obj.destination_label,
            },
        )


@admin.register(FinancialRoutingLog)
class FinancialRoutingLogAdmin(admin.ModelAdmin):

    list_display = (
        "rule",
        "action",
        "performed_by",
        "created_at",
    )

    list_filter = (
        "action",
        "created_at",
    )

    search_fields = (
        "rule__country_code",
        "rule__country_name",
        "rule__currency_code",
        "rule__source_name",
        "rule__partner_name",
        "rule__destination_label",
        "performed_by__username",
    )

    readonly_fields = (
        "rule",
        "action",
        "performed_by",
        "details",
        "created_at",
    )

    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FinancialFeeRule)
class FinancialFeeRuleAdmin(admin.ModelAdmin):

    list_display = (
        "fee_type",
        "percentage",
        "active",
        "updated_at",
    )

    list_filter = (
        "fee_type",
        "active",
    )

    search_fields = (
        "fee_type",
        "description",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = (
        "fee_type",
    )
