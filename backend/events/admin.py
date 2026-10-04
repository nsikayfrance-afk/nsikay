from django.contrib import admin

from .models import (
    Event,
    EventTicket,
    EventRegistration,
    EventMediaLink,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "city",
        "start_at",
        "status",
        "is_free",
        "featured",
    )

    list_filter = (
        "status",
        "mode",
        "is_free",
        "featured",
        "category",
    )

    search_fields = (
        "title",
        "description",
        "city",
        "venue",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }


@admin.register(EventTicket)
class EventTicketAdmin(admin.ModelAdmin):

    list_display = (
        "event",
        "name",
        "price",
        "currency",
        "quantity",
        "active",
    )

    list_filter = ("active", "currency")
    search_fields = ("name", "event__title")


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):

    list_display = (
        "event",
        "user",
        "ticket",
        "quantity",
        "status",
        "created_at",
    )

    list_filter = ("status",)
    search_fields = (
        "event__title",
        "user__username",
    )


@admin.register(EventMediaLink)
class EventMediaLinkAdmin(admin.ModelAdmin):

    list_display = (
        "event",
        "media_asset_id",
        "role",
        "active",
        "created_at",
    )

    list_filter = ("active", "role")
    search_fields = ("event__title",)
