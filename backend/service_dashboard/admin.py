from django.contrib import admin
from .models import ServiceDashboardLog


@admin.register(ServiceDashboardLog)
class ServiceDashboardLogAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "country",
        "action",
        "admin_user",
        "created_at",
    )

