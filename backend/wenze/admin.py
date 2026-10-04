from django.contrib import admin

from .models import BukaPrixCampaign, WenzeOrder, WenzeProduct


@admin.register(WenzeProduct)
class WenzeProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "seller",
        "price",
        "currency",
        "stock",
        "status",
        "created_at",
    )
    list_filter = ("status", "currency")
    search_fields = ("name", "description", "seller__username")


@admin.register(WenzeOrder)
class WenzeOrderAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "buyer",
        "product",
        "quantity",
        "total_amount",
        "currency",
        "status",
        "created_at",
    )
    list_filter = ("status", "currency")
    search_fields = (
        "reference",
        "buyer__username",
        "product__name",
    )
    readonly_fields = (
        "reference",
        "created_at",
        "updated_at",
    )


@admin.register(BukaPrixCampaign)
class BukaPrixCampaignAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "product",
        "promotion_price",
        "start_at",
        "end_at",
        "active",
        "created_by",
    )
    list_filter = ("active",)
    search_fields = ("title", "product__name")
