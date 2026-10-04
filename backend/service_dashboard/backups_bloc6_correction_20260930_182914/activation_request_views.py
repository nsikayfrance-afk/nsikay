from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from service_control.models import (
    GlobalService,
    CountryServiceStatus,
)

from service_dashboard.models import (
    ServiceActivationRequest,
    ServiceDashboardLog,
)

from .activation_request_services import (
    ActivationRequestManager,
    ActivationRequestValidator,
)


def _is_nsikay_admin(user):
    if not user or not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    groups = set(
        user.groups.values_list("name", flat=True)
    )

    allowed_groups = {
        "Super Administrateur",
        "Administration Pays",
        "Administration NSIKAY",
        "Administrateur NSIKAY",
    }

    return bool(groups.intersection(allowed_groups))


@login_required
@require_POST
def create_activation_request(request):
    if not _is_nsikay_admin(request.user):
        return HttpResponseForbidden(
            "Accès réservé à l'administration NSIKAY."
        )

    service_id = request.POST.get("service_id")
    country_id = request.POST.get("country_id")

    if not service_id or not country_id:
        return JsonResponse(
            {
                "allowed": False,
                "message": "service_id et country_id sont obligatoires.",
            },
            status=400,
        )

    service = get_object_or_404(
        GlobalService,
        pk=service_id,
    )

    country = get_object_or_404(
        CountryServiceStatus,
        pk=country_id,
    )

    with transaction.atomic():

        result = ActivationRequestValidator.validate(
            service,
            country,
            request.user,
        )

        activation_request, created, message = (
            ActivationRequestManager.create(
                service,
                country,
                request.user,
                request.POST.get("reason", ""),
            )
        )

        return JsonResponse(
            {
                "request_id": activation_request.id,
                "created": created,
                "status": activation_request.status,
                "allowed_for_validation": result.allowed,
                "message": message,
                "activation_executed": False,
            }
        )


@login_required
@require_POST
def validate_activation_request(request, request_id):
    if not _is_nsikay_admin(request.user):
        return HttpResponseForbidden(
            "Accès réservé à l'administration NSIKAY."
        )

    with transaction.atomic():

        activation_request = (
            ServiceActivationRequest.objects
            .select_for_update()
            .select_related("service", "country", "requested_by")
            .get(pk=request_id)
        )

        if activation_request.status != "pending":
            return JsonResponse(
                {
                    "allowed": False,
                    "message": (
                        "Cette demande n'est plus en attente."
                    ),
                },
                status=400,
            )

        result = ActivationRequestValidator.validate(
            activation_request.service,
            activation_request.country,
            activation_request.requested_by,
        )

        if not result.allowed:
            activation_request.admin_validated = False
            activation_request.validation_message = result.message
            activation_request.rejection_reason = result.message
            activation_request.status = "rejected"

            activation_request.certification_checked = (
                result.certification_checked
            )
            activation_request.health_insurance_checked = (
                result.health_insurance_checked
            )
            activation_request.bank_partner_checked = (
                result.bank_partner_checked
            )
            activation_request.financial_partner_checked = (
                result.financial_partner_checked
            )
            activation_request.country_authorization_checked = (
                result.country_authorization_checked
            )

            activation_request.save()

            ServiceDashboardLog.objects.create(
                action="activation_request_rejected",
                admin_user=str(request.user),
                comment=result.message,
                country=activation_request.country,
                service=activation_request.service,
            )

            return JsonResponse(
                {
                    "allowed": False,
                    "status": "rejected",
                    "request_id": activation_request.id,
                    "message": result.message,
                    "activation_executed": False,
                }
            )

        activation_request.admin_validated = True
        activation_request.validation_message = result.message
        activation_request.rejection_reason = ""

        activation_request.certification_checked = True
        activation_request.health_insurance_checked = True
        activation_request.bank_partner_checked = True
        activation_request.financial_partner_checked = True
        activation_request.country_authorization_checked = True

        activation_request.status = "approved"
        activation_request.validated_at = (
            __import__("django.utils.timezone", fromlist=["timezone"])
            .timezone.now()
        )

        activation_request.save()

        ServiceDashboardLog.objects.create(
            action="activation_request_approved",
            admin_user=str(request.user),
            comment=(
                "Demande validée par l'administration. "
                "Aucune activation automatique exécutée."
            ),
            country=activation_request.country,
            service=activation_request.service,
        )

        return JsonResponse(
            {
                "allowed": True,
                "status": "approved",
                "request_id": activation_request.id,
                "message": result.message,
                "activation_executed": False,
            }
        )


@login_required
@require_POST
def reject_activation_request(request, request_id):
    if not _is_nsikay_admin(request.user):
        return HttpResponseForbidden(
            "Accès réservé à l'administration NSIKAY."
        )

    reason = (request.POST.get("reason") or "").strip()

    if not reason:
        return JsonResponse(
            {
                "allowed": False,
                "message": (
                    "Le motif de refus est obligatoire."
                ),
            },
            status=400,
        )

    with transaction.atomic():

        activation_request = (
            ServiceActivationRequest.objects
            .select_for_update()
            .select_related("service", "country")
            .get(pk=request_id)
        )

        if activation_request.status != "pending":
            return JsonResponse(
                {
                    "allowed": False,
                    "message": (
                        "Cette demande n'est plus en attente."
                    ),
                },
                status=400,
            )

        activation_request.status = "rejected"
        activation_request.admin_validated = False
        activation_request.rejection_reason = reason
        activation_request.validation_message = (
            "Demande refusée par l'administration."
        )
        activation_request.save()

        ServiceDashboardLog.objects.create(
            action="activation_request_rejected",
            admin_user=str(request.user),
            comment=reason,
            country=activation_request.country,
            service=activation_request.service,
        )

        return JsonResponse(
            {
                "allowed": False,
                "status": "rejected",
                "request_id": activation_request.id,
                "message": reason,
                "activation_executed": False,
            }
        )
