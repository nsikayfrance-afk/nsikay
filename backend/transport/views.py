from rest_framework.decorators import action
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

    @action(
        detail=True,
        methods=["post"],
        url_path="validate",
    )
    def validate_company(self, request, pk=None):
        """
        Validation administrative de l'entreprise.

        Cette étape ne remplace pas la certification.
        L'entreprise doit ensuite être activée explicitement.
        """
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {
                    "detail": (
                        "La validation administrative "
                        "est réservée à l'administration NSIKAY."
                    )
                },
                status=403,
            )

        company = self.get_object()

        company.validated_by_admin = True
        company.save(
            update_fields=[
                "validated_by_admin",
                "updated_at",
            ]
        )

        return Response(
            {
                "success": True,
                "id": company.id,
                "validated_by_admin": True,
                "active": company.active,
                "certification_status": (
                    company.certification.status
                    if company.certification
                    else None
                ),
                "message": (
                    "Entreprise validée administrativement. "
                    "L'activation reste soumise à la certification NSIKAY."
                ),
            }
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="activate",
    )
    def activate_company(self, request, pk=None):
        """
        Activation administrative finale.

        Conditions :
        - certification obligatoire approuvée ;
        - validation administrative effectuée.
        """
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {
                    "detail": (
                        "L'activation est réservée "
                        "à l'administration NSIKAY."
                    )
                },
                status=403,
            )

        company = self.get_object()

        try:
            ensure_company_activation_allowed(company)
        except ValidationError as exc:
            return Response(
                {
                    "success": False,
                    "detail": str(exc),
                    "certification_status": (
                        company.certification.status
                        if company.certification
                        else None
                    ),
                    "validated_by_admin": company.validated_by_admin,
                    "active": company.active,
                },
                status=400,
            )

        company.active = True
        company.save(
            update_fields=[
                "active",
                "updated_at",
            ]
        )

        return Response(
            {
                "success": True,
                "id": company.id,
                "active": True,
                "validated_by_admin": company.validated_by_admin,
                "certification_status": (
                    company.certification.status
                    if company.certification
                    else None
                ),
                "message": (
                    "Entreprise de transport activée avec succès."
                ),
            }
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="deactivate",
    )
    def deactivate_company(self, request, pk=None):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {
                    "detail": (
                        "La désactivation est réservée "
                        "à l'administration NSIKAY."
                    )
                },
                status=403,
            )

        company = self.get_object()

        company.active = False
        company.save(
            update_fields=[
                "active",
                "updated_at",
            ]
        )

        return Response(
            {
                "success": True,
                "id": company.id,
                "active": False,
                "message": (
                    "Entreprise de transport désactivée."
                ),
            }
        )
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

from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from business.models import Company


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def transport_onboarding(request):
    """
    Inscription réelle d'une entreprise de transport NSIKAY.

    GET:
        Retourne l'état réel de l'onboarding de l'utilisateur.

    POST:
        Crée :
        - une Company réelle appartenant à l'utilisateur ;
        - une NSIKAYCertification en attente ;
        - une TransportCompany inactive.

    Aucune activation automatique.
    """

    if request.method == "GET":

        companies = Company.objects.filter(
            owner=request.user
        ).distinct()

        transport_companies = TransportCompany.objects.filter(
            company__in=companies
        ).select_related(
            "company",
            "certification"
        )

        return Response({
            "service": "NSIKAY Transport",
            "certification_required": True,
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            },
            "steps": [
                {
                    "key": "company",
                    "label": "Entreprise",
                    "status": "required"
                },
                {
                    "key": "transport_type",
                    "label": "Type de transport",
                    "status": "required"
                },
                {
                    "key": "services",
                    "label": "Services",
                    "status": "required"
                },
                {
                    "key": "vehicles",
                    "label": "Véhicules",
                    "status": "optional"
                },
                {
                    "key": "drivers",
                    "label": "Conducteurs",
                    "status": "optional"
                },
                {
                    "key": "certification",
                    "label": "Certification NSIKAY",
                    "status": "required"
                },
                {
                    "key": "administrative_validation",
                    "label": "Validation administrative",
                    "status": "required"
                },
                {
                    "key": "activation",
                    "label": "Activation",
                    "status": "required"
                },
            ],
            "transport_companies": [
                {
                    "id": item.id,
                    "company_id": item.company_id,
                    "company_name": (
                        item.company.name
                        if item.company
                        else ""
                    ),
                    "transport_type": item.transport_type,
                    "country": item.country,
                    "city": item.city,
                    "certification_required": item.certification_required,
                    "certification_status": (
                        item.certification.status
                        if item.certification
                        else None
                    ),
                    "validated_by_admin": item.validated_by_admin,
                    "active": item.active,
                }
                for item in transport_companies
            ],
        }, status=status.HTTP_200_OK)

    # ========================================================
    # POST - CREATION REELLE DE L'INSCRIPTION
    # ========================================================

    data = request.data

    name = str(data.get("name", "")).strip()
    description = str(data.get("description", "")).strip()
    transport_type = str(
        data.get("transport_type", "")
    ).strip().upper()

    country = str(data.get("country", "")).strip()
    city = str(data.get("city", "")).strip()

    phone = str(data.get("phone", "")).strip()
    email = str(
        data.get("email", request.user.email or "")
    ).strip()

    website = str(data.get("website", "")).strip()

    allowed_transport_types = {
        "GOODS",
        "PASSENGER",
        "BOTH",
    }

    errors = {}

    if not name:
        errors["name"] = "Le nom de l'entreprise est obligatoire."

    if transport_type not in allowed_transport_types:
        errors["transport_type"] = (
            "Le type de transport doit être GOODS, PASSENGER ou BOTH."
        )

    if not country:
        errors["country"] = "Le pays est obligatoire."

    if not city:
        errors["city"] = "La ville est obligatoire."

    if errors:
        return Response(
            {
                "detail": "Les données d'inscription sont incomplètes.",
                "errors": errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Import local pour éviter de modifier inutilement
    # l'ordre des imports existants de views.py.
    from certification.models import NSIKAYCertification

    # Une entreprise de transport déjà enregistrée pour
    # cet utilisateur ne doit pas être recréée.
    existing = TransportCompany.objects.filter(
        company__owner=request.user
    ).select_related(
        "company",
        "certification"
    ).first()

    if existing:
        return Response(
            {
                "detail": (
                    "Une entreprise de transport est déjà "
                    "enregistrée pour ce compte."
                ),
                "transport_company_id": existing.id,
                "company_id": existing.company_id,
                "certification_status": (
                    existing.certification.status
                    if existing.certification
                    else None
                ),
                "active": existing.active,
            },
            status=status.HTTP_409_CONFLICT,
        )

    with transaction.atomic():

        # ----------------------------------------------------
        # 1. ENTREPRISE
        # ----------------------------------------------------

        business_company = Company.objects.create(
            owner=request.user,
            name=name,
            description=description,
            verified=False,
        )

        # ----------------------------------------------------
        # 2. CERTIFICATION NSIKAY
        # ----------------------------------------------------

        certification = NSIKAYCertification.objects.create(
            owner=request.user,
            certification_type="company",
            activity=(
                f"Transport - {name} - "
                f"{transport_type}"
            ),
            document_reference=(
                f"TRANSPORT-{request.user.id}-"
                f"{business_company.id}"
            ),
            status="pending",
        )

        # ----------------------------------------------------
        # 3. ENTREPRISE DE TRANSPORT
        # ----------------------------------------------------

        transport_company = TransportCompany.objects.create(
            company=business_company,
            transport_type=transport_type,
            description=description,
            phone=phone,
            email=email,
            website=website,
            country=country,
            city=city,
            certification=certification,
            certification_required=True,
            active=False,
            validated_by_admin=False,
        )

    return Response(
        {
            "detail": (
                "Inscription de l'entreprise de transport "
                "enregistrée avec succès."
            ),
            "service": "NSIKAY Transport",
            "transport_company": {
                "id": transport_company.id,
                "company_id": business_company.id,
                "company_name": business_company.name,
                "transport_type": transport_company.transport_type,
                "country": transport_company.country,
                "city": transport_company.city,
                "active": transport_company.active,
                "validated_by_admin": (
                    transport_company.validated_by_admin
                ),
            },
            "certification": {
                "id": certification.id,
                "status": certification.status,
                "type": certification.certification_type,
            },
            "workflow": [
                "Inscription enregistrée",
                "Certification NSIKAY en attente",
                "Validation par l'Autorité Certification",
                "Validation administrative",
                "Activation de l'entreprise",
            ],
        },
        status=status.HTTP_201_CREATED,
    )
