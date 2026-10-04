from django.contrib import admin

from .models import Activity, Service, Project


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "activity_type",
        "profile",
        "status",
        "certification_status",
        "created_at",
    )
    list_filter = (
        "activity_type",
        "status",
        "certification_status",
        "visibility",
    )
    search_fields = (
        "name",
        "sector",
        "country",
        "city",
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "activity",
        "price",
        "currency",
        "status",
        "certification_status",
    )
    list_filter = (
        "status",
        "certification_status",
    )
    search_fields = (
        "name",
        "category",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "activity",
        "status",
        "start_date",
        "end_date",
    )
    list_filter = ("status",)
    search_fields = ("name",)
