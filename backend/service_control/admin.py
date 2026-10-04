from django.contrib import admin
from .models import (
    CountryServiceStatus,
    GlobalService,
    ServiceActivation,
    ServiceRule,
)


@admin.register(CountryServiceStatus)
class CountryServiceStatusAdmin(admin.ModelAdmin):
    list_display = (
        "country_code",
        "country_name",
    )
    search_fields = (
        "country_code",
        "country_name",
    )
    ordering = ("country_name",)


@admin.register(GlobalService)
class GlobalServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "active_global",
    )
    list_filter = (
        "category",
        "active_global",
    )
    search_fields = (
        "name",
        "category",
    )
    ordering = ("category", "name")


@admin.register(ServiceActivation)
class ServiceActivationAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "country",
        "active",
        "validated_by_admin",
        "reason",
    )
    list_filter = (
        "active",
        "validated_by_admin",
        "service",
    )
    search_fields = (
        "service__name",
        "country__country_name",
        "country__country_code",
        "reason",
    )
    list_select_related = (
        "service",
        "country",
    )


@admin.register(ServiceRule)
class ServiceRuleAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "certification_required",
        "partner_bank_required",
        "financial_partner_required",
        "health_insurance_required",
        "remote_activation_allowed",
        "admin_validation_required",
        "country_authorization_required",
        "active_by_default",
    )
    list_filter = (
        "certification_required",
        "partner_bank_required",
        "financial_partner_required",
        "health_insurance_required",
        "remote_activation_allowed",
        "admin_validation_required",
        "country_authorization_required",
        "active_by_default",
    )
    search_fields = (
        "service__name",
        "service__category",
        "description",
    )
    list_select_related = (
        "service",
    )

