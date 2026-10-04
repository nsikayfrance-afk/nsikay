from django.contrib import admin
from .models import AdminAuditLog


@admin.register(AdminAuditLog)
class AdminAuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "action",
        "module",
        "created_at",
    )

    search_fields = (
        "module",
        "action",
    )

