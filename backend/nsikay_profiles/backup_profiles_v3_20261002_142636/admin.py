from django.contrib import admin

from .models import NsikayProfile


@admin.register(NsikayProfile)
class NsikayProfileAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "profile_type",
        "user",
        "country",
        "status",
        "visibility",
        "is_primary",
        "certification_required",
    )

    list_filter = (
        "profile_type",
        "status",
        "visibility",
        "certification_required",
    )

    search_fields = (
        "display_name",
        "legal_name",
        "professional_title",
        "country",
        "city",
        "sector",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
