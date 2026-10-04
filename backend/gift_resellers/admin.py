from django.contrib import admin

from .models import (
    DistributionAgreement,
    GiftInventoryUnit,
    GiftResellerAuditLog,
    NetworkMember,
    Reseller,
    ResellerNetwork,
    ResellerSale,
    SaleAllocation,
)


@admin.register(Reseller)
class ResellerAdmin(admin.ModelAdmin):
    list_display = (
        "reseller_code",
        "user",
        "status",
        "country_code",
        "created_at",
    )
    list_filter = ("status", "country_code")
    search_fields = ("reseller_code", "user__username", "user__email")


@admin.register(ResellerNetwork)
class ResellerNetworkAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "principal_reseller",
        "active",
        "created_at",
    )
    list_filter = ("active",)
    search_fields = ("code", "name")


@admin.register(NetworkMember)
class NetworkMemberAdmin(admin.ModelAdmin):
    list_display = (
        "network",
        "user",
        "active",
        "joined_at",
    )
    list_filter = ("active",)
    search_fields = (
        "network__code",
        "user__username",
        "user__email",
    )


@admin.register(GiftInventoryUnit)
class GiftInventoryUnitAdmin(admin.ModelAdmin):
    list_display = (
        "unit_id",
        "gift",
        "official_value_eur",
        "source",
        "credit_only",
        "status",
        "current_reseller",
        "current_member",
    )
    list_filter = (
        "source",
        "credit_only",
        "status",
    )
    search_fields = (
        "unit_id",
        "gift__name",
    )
    readonly_fields = (
        "official_value_eur",
        "currency_reference",
        "created_at",
        "updated_at",
    )


@admin.register(DistributionAgreement)
class DistributionAgreementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "principal_reseller",
        "network_member",
        "gift",
        "quantity",
        "member_percentage",
        "principal_reseller_percentage",
        "nsikay_percentage",
        "status",
        "version",
    )
    list_filter = ("status", "gift")
    readonly_fields = (
        "created_at",
        "accepted_at",
        "locked_at",
    )


@admin.register(ResellerSale)
class ResellerSaleAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "gift_unit",
        "customer",
        "retail_amount",
        "retail_currency",
        "official_value_eur",
        "nsikay_amount_eur",
        "member_amount",
        "principal_reseller_amount",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "retail_currency",
    )
    search_fields = (
        "reference",
        "payment_reference",
        "gift_unit__unit_id",
    )
    readonly_fields = (
        "created_at",
        "settled_at",
    )


@admin.register(SaleAllocation)
class SaleAllocationAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "sale",
        "allocation_type",
        "percentage",
        "base_amount",
        "amount",
        "currency",
        "created_at",
    )
    list_filter = (
        "allocation_type",
        "currency",
    )
    search_fields = (
        "reference",
        "sale__reference",
    )
    readonly_fields = (
        "created_at",
    )


@admin.register(GiftResellerAuditLog)
class GiftResellerAuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "action",
        "reference",
        "actor",
    )
    list_filter = ("action",)
    search_fields = (
        "reference",
        "actor__username",
    )
    readonly_fields = (
        "created_at",
    )