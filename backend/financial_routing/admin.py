from django.contrib import admin

from .models import (
    FinancialPartner,
    FinancialRoutingRule,
    FinancialRoutingLog,
    FinancialFeeRule,
)

from .services import (
    approve_routing_rule,
    suspend_routing_rule,
    activate_routing_rule,
)


# ============================================================
# ACTIONS ADMINISTRATIVES
# ============================================================

@admin.action(description="Approuver les règles sélectionnées")
def approve_selected_routing_rules(modeladmin, request, queryset):

    count = 0

    for rule in queryset:

        approve_routing_rule(
            rule,
            user=request.user,
            details={
                "source": "django_admin",
                "action": "APPROVE_SELECTED",
            },
        )

        count += 1

    modeladmin.message_user(
        request,
        f"{count} règle(s) de routage approuvée(s).",
    )


@admin.action(description="Suspendre les règles sélectionnées")
def suspend_selected_routing_rules(modeladmin, request, queryset):

    count = 0

    for rule in queryset:

        suspend_routing_rule(
            rule,
            user=request.user,
            details={
                "source": "django_admin",
                "action": "SUSPEND_SELECTED",
            },
        )

        count += 1

    modeladmin.message_user(
        request,
        f"{count} règle(s) de routage suspendue(s).",
    )


@admin.action(description="Réactiver les règles sélectionnées")
def activate_selected_routing_rules(modeladmin, request, queryset):

    count = 0

    for rule in queryset:

        activate_routing_rule(
            rule,
            user=request.user,
            details={
                "source": "django_admin",
                "action": "ACTIVATE_SELECTED",
            },
        )

        count += 1

    modeladmin.message_user(
        request,
        f"{count} règle(s) de routage réactivée(s).",
    )


# ============================================================
# FINANCIAL PARTNER
# ============================================================

@admin.register(FinancialPartner)
class FinancialPartnerAdminNSIKAY(admin.ModelAdmin):

    list_display = (
        "name",
        "partner_type",
        "country_code",
        "status",
        "certified",
        "active",
        "bank",
        "partner_application",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "partner_type",
        "status",
        "certified",
        "active",
        "country_code",
    )

    search_fields = (
        "name",
        "legal_name",
        "country_code",
        "country_name",
        "external_reference",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "created_by",
        "approved_by",
    )


# ============================================================
# FINANCIAL ROUTING RULE
# ============================================================

@admin.register(FinancialRoutingRule)
class FinancialRoutingRuleAdminNSIKAY(admin.ModelAdmin):

    list_display = (
        "source_type",
        "operation_type",
        "country_code",
        "currency_code",
        "partner_type",
        "partner_name",
        "priority",
        "active",
        "status",
        "created_at",
    )

    list_filter = (
        "source_type",
        "operation_type",
        "partner_type",
        "status",
        "active",
        "country_code",
        "currency_code",
    )

    search_fields = (
        "source_name",
        "partner_name",
        "bank_name",
        "bank_country",
        "destination_label",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "created_by",
        "approved_by",
    )

    actions = (
        approve_selected_routing_rules,
        suspend_selected_routing_rules,
        activate_selected_routing_rules,
    )


# ============================================================
# FINANCIAL ROUTING LOG
# ============================================================

@admin.register(FinancialRoutingLog)
class FinancialRoutingLogAdminNSIKAY(admin.ModelAdmin):

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
        "rule__partner_name",
        "details",
    )

    readonly_fields = (
        "created_at",
    )


# ============================================================
# FINANCIAL FEE RULE
# ============================================================

@admin.register(FinancialFeeRule)
class FinancialFeeRuleAdminNSIKAY(admin.ModelAdmin):

    list_display = (
        "fee_type",
        "percentage",
        "active",
        "description",
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
