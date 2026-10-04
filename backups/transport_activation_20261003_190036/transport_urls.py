from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TransportCompanyViewSet,
    TransportVehicleViewSet,
    TransportDriverViewSet,
    TransportServiceViewSet,
    WenzeDeliveryViewSet,
    PassengerRideViewSet,
    PassengerRentalViewSet,
    TransportTrackingEventViewSet,
    transport_dashboard,
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
        "dashboard/",
        transport_dashboard,
        name="transport-dashboard",
    ),
    path(
        "",
        include(router.urls),
    ),
]