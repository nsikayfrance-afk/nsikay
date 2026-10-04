from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    transport_dashboard,
    transport_onboarding,
    TransportCompanyViewSet,
    TransportVehicleViewSet,
    TransportDriverViewSet,
    TransportServiceViewSet,
    WenzeDeliveryViewSet,
    PassengerRideViewSet,
    PassengerRentalViewSet,
    TransportTrackingEventViewSet,
)

router = DefaultRouter()

router.register(
    r"companies",
    TransportCompanyViewSet,
    basename="transport-company",
)

router.register(
    r"vehicles",
    TransportVehicleViewSet,
    basename="transport-vehicle",
)

router.register(
    r"drivers",
    TransportDriverViewSet,
    basename="transport-driver",
)

router.register(
    r"services",
    TransportServiceViewSet,
    basename="transport-service",
)

router.register(
    r"marchandises/livraisons",
    WenzeDeliveryViewSet,
    basename="wenze-delivery",
)

router.register(
    r"personnes/courses",
    PassengerRideViewSet,
    basename="passenger-ride",
)

router.register(
    r"personnes/locations",
    PassengerRentalViewSet,
    basename="passenger-rental",
)

router.register(
    r"tracking",
    TransportTrackingEventViewSet,
    basename="transport-tracking",
)

urlpatterns = [
    path(
        "onboarding/",
        transport_onboarding,
        name="transport-onboarding",
    ),
    path(
        "dashboard/",
        transport_dashboard,
        name="transport-dashboard",
    ),
    path(
        "",
        include(router.urls),
    ),
]