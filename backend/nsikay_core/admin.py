from django.contrib import admin
from .models import (
    NsikayCountry,
    ActivityDomain,
    ActorProfile,
    ActorCertification
)


@admin.register(NsikayCountry)
class NsikayCountryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'active'
    )
    search_fields = (
        'name',
        'code'
    )


@admin.register(ActivityDomain)
class ActivityDomainAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(ActorProfile)
class ActorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'country',
        'activity',
        'actor_type',
        'certified'
    )
    list_filter = (
        'country',
        'activity',
        'actor_type',
        'certified'
    )


@admin.register(ActorCertification)
class ActorCertificationAdmin(admin.ModelAdmin):
    list_display = (
        'actor',
        'status',
        'issued_date',
        'expiry_date'
    )
    list_filter = (
        'status',
    )

