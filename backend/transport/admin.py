from django.contrib import admin

from .models import (
    TransportCompany,
    TransportVehicle,
    TransportDriver,
    TransportService,
    WenzeDelivery,
    PassengerRide,
    PassengerRental,
    TransportTrackingEvent,
)


@admin.register(TransportCompany)
class TransportCompanyAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "transport_type",
        "country",
        "city",
        "active",
        "validated_by_admin",
    )

    list_filter = (
        "transport_type",
        "active",
        "validated_by_admin",
        "country",
    )

    search_fields = (
        "company__name",
        "country",
        "city",
    )


@admin.register(TransportVehicle)
class TransportVehicleAdmin(admin.ModelAdmin):
    list_display = (
        "registration_number",
        "transport_company",
        "vehicle_type",
        "status",
        "active",
    )

    list_filter = (
        "vehicle_type",
        "status",
        "active",
    )

    search_fields = (
        "registration_number",
        "brand",
        "model",
    )


@admin.register(TransportDriver)
class TransportDriverAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "transport_company",
        "license_number",
        "validated",
        "active",
    )

    list_filter = (
        "validated",
        "active",
    )

    search_fields = (
        "license_number",
        "phone",
        "user__username",
    )


@admin.register(TransportService)
class TransportServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "transport_company",
        "service_type",
        "pricing_mode",
        "active",
    )

    list_filter = (
        "service_type",
        "pricing_mode",
        "active",
    )

    search_fields = (
        "name",
        "transport_company__company__name",
    )


@admin.register(WenzeDelivery)
class WenzeDeliveryAdmin(admin.ModelAdmin):
    list_display = (
        "tracking_reference",
        "order",
        "transport_company",
        "vehicle",
        "driver",
        "status",
    )

    list_filter = ("status",)

    search_fields = (
        "tracking_reference",
        "order__reference",
        "recipient_name",
        "recipient_phone",
    )


@admin.register(PassengerRide)
class PassengerRideAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "passenger",
        "transport_company",
        "driver",
        "status",
        "requested_at",
    )

    list_filter = ("status",)

    search_fields = (
        "reference",
        "passenger__username",
        "pickup_address",
        "destination_address",
    )


@admin.register(PassengerRental)
class PassengerRentalAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "passenger",
        "transport_company",
        "vehicle",
        "status",
        "start_at",
        "end_at",
    )

    list_filter = ("status",)

    search_fields = (
        "reference",
        "passenger__username",
        "pickup_address",
    )


@admin.register(TransportTrackingEvent)
class TransportTrackingEventAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "location",
        "delivery",
        "ride",
        "rental",
        "created_at",
    )

    list_filter = ("status",)

    search_fields = (
        "status",
        "location",
        "note",
    )