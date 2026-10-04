# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.



from django.contrib import admin
from .models import VirtualGift

@admin.register(VirtualGift)
class VirtualGiftAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "value_eur",
        "currency_reference",
        "category",
        "active",
        "display_order",
    )
    list_filter = (
        "active",
        "category",
        "currency_reference",
    )
    search_fields = (
        "name",
        "slug",
    )
    ordering = (
        "display_order",
        "value_eur",
    )
    readonly_fields = ()
