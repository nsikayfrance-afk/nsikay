from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

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

from .serializers import (
    TransportCompanySerializer,
    TransportVehicleSerializer,
    TransportDriverSerializer,
    TransportServiceSerializer,
    WenzeDeliverySerializer,
    PassengerRideSerializer,
    PassengerRentalSerializer,
    TransportTrackingEventSerializer,
)
from .rules import (
    ensure_company_activation_allowed,
    ensure_transport_company_is_active,
)


class TransportCompanyViewSet(viewsets.ModelViewSet):
    queryset = TransportCompany.objects.select_related(
        "company",
        "certification",
    ).all()
    serializer_class = TransportCompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class TransportVehicleViewSet(viewsets.ModelViewSet):
    queryset = TransportVehicle.objects.select_related(
        "transport_company",
    ).all()
    serializer_class = TransportVehicleSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransportDriverViewSet(viewsets.ModelViewSet):
    queryset = TransportDriver.objects.select_related(
        "transport_company",
        "user",
    ).all()
    serializer_class = TransportDriverSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransportServiceViewSet(viewsets.ModelViewSet):
    queryset = TransportService.objects.select_related(
        "transport_company",
        "currency",
    ).all()
    serializer_class = TransportServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class WenzeDeliveryViewSet(viewsets.ModelViewSet):
    queryset = WenzeDelivery.objects.select_related(
        "order",
        "transport_company",
        "vehicle",
        "driver",
    ).all()
    serializer_class = WenzeDeliverySerializer
    permission_classes = [permissions.IsAuthenticated]


class PassengerRideViewSet(viewsets.ModelViewSet):
    queryset = PassengerRide.objects.select_related(
        "passenger",
        "transport_company",
        "service",
        "vehicle",
        "driver",
        "currency",
    ).all()
    serializer_class = PassengerRideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_superuser or self.request.user.is_staff:
            return queryset

        return queryset.filter(passenger=self.request.user)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)


class PassengerRentalViewSet(viewsets.ModelViewSet):
    queryset = PassengerRental.objects.select_related(
        "passenger",
        "transport_company",
        "service",
        "vehicle",
        "currency",
    ).all()
    serializer_class = PassengerRentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_superuser or self.request.user.is_staff:
            return queryset

        return queryset.filter(passenger=self.request.user)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)


class TransportTrackingEventViewSet(viewsets.ModelViewSet):
    queryset = TransportTrackingEvent.objects.select_related(
        "delivery",
        "ride",
        "rental",
    ).all()
    serializer_class = TransportTrackingEventSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def transport_dashboard(request):

    return Response(
        {
            "transport": {
                "entreprises": TransportCompany.objects.count(),
                "vehicules": TransportVehicle.objects.count(),
                "conducteurs": TransportDriver.objects.count(),
                "services": TransportService.objects.count(),
                "livraisons_wenze": WenzeDelivery.objects.count(),
                "courses_personnes": PassengerRide.objects.count(),
                "locations_journee": PassengerRental.objects.count(),
                "suivis": TransportTrackingEvent.objects.count(),
            },
            "categories": {
                "marchandises": {
                    "service": "WENZE",
                    "description": "Transport des commandes et marchandises WENZE.",
                },
                "personnes": {
                    "course": "Commande d'un trajet",
                    "location": "Reservation d'une voiture a la journee",
                },
            },
            "certification": {
                "obligatoire": True,
                "source": "NSIKAYCertification",
            },
        }
    )