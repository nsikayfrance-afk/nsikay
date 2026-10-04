from dataclasses import dataclass
from django.db import transaction
from django.utils import timezone

from service_control.models import (
    GlobalService,
    CountryServiceStatus,
    ServiceActivation,
    ServiceRule,
)
from service_dashboard.models import (
    ServiceActivationRequest,
    ServiceDashboardLog,
)


@dataclass
class OperationalValidationResult:
    allowed: bool
    message: str
    service: object = None
    country: object = None
    activation: object = None


class OperationalValidationService:

    @staticmethod
    def load(service_id, country_id):
        service = GlobalService.objects.filter(
            id=service_id
        ).first()

        country = CountryServiceStatus.objects.filter(
            id=country_id
        ).first()

        if not service:
            return None, None, "Service introuvable."

        if not country:
            return None, None, "Pays introuvable."

        return service, country, ""

    @staticmethod
    def validate_relation(service, country):

        activation = ServiceActivation.objects.filter(
            service=service,
            country=country,
        ).select_related(
            "service",
            "country",
        ).first()

        if not activation:
            return OperationalValidationResult(
                False,
                "La relation service/pays n'existe pas.",
                service,
                country,
                None,
            )

        if not country.is_primary:
            return OperationalValidationResult(
                False,
                "Le pays n'est pas un pays primaire NSIKAY.",
                service,
                country,
                activation,
            )

        if not country.is_operational:
            return OperationalValidationResult(
                False,
                "Le pays n'est pas actuellement operationnel.",
                service,
                country,
                activation,
            )

        rule = ServiceRule.objects.filter(
            service=service
        ).first()

        if not rule:
            return OperationalValidationResult(
                False,
                "Aucune regle de service n'est configuree.",
                service,
                country,
                activation,
            )

        return OperationalValidationResult(
            True,
            "Relation service/pays operationnelle et regle presente.",
            service,
            country,
            activation,
        )

    @staticmethod
    def validate_request(request_id):

        request = ServiceActivationRequest.objects.select_related(
            "service",
            "country",
            "requested_by",
            "beneficiary_user",
        ).filter(
            id=request_id
        ).first()

        if not request:
            return OperationalValidationResult(
                False,
                "Demande d'activation introuvable.",
            )

        result = OperationalValidationService.validate_relation(
            request.service,
            request.country,
        )

        return result

    @staticmethod
    @transaction.atomic
    def approve_request(request_id, admin_user, comment=""):

        request = ServiceActivationRequest.objects.select_for_update().select_related(
            "service",
            "country",
            "requested_by",
            "beneficiary_user",
        ).filter(
            id=request_id
        ).first()

        if not request:
            return False, "Demande introuvable.", None

        if request.status != "pending":
            return False, "La demande n'est plus en attente.", request

        result = OperationalValidationService.validate_relation(
            request.service,
            request.country,
        )

        if not result.allowed:
            request.status = "rejected"
            request.admin_validated = False
            request.rejection_reason = result.message
            request.validation_message = result.message
            request.validated_at = timezone.now()
            request.save(
                update_fields=[
                    "status",
                    "admin_validated",
                    "rejection_reason",
                    "validation_message",
                    "validated_at",
                    "updated_at",
                ]
            )

            ServiceDashboardLog.objects.create(
                action="reject",
                service=request.service,
                country=request.country,
                admin=admin_user,
                comment=result.message,
            )

            return False, result.message, request

        request.status = "validated"
        request.admin_validated = True
        request.validation_message = comment or result.message
        request.validated_at = timezone.now()
        request.save(
            update_fields=[
                "status",
                "admin_validated",
                "validation_message",
                "validated_at",
                "updated_at",
            ]
        )

        ServiceDashboardLog.objects.create(
            action="validate",
            service=request.service,
            country=request.country,
            admin=admin_user,
            comment=comment or result.message,
        )

        return True, request.validation_message, request

    @staticmethod
    @transaction.atomic
    def activate_validated_request(request_id, admin_user, comment=""):

        request = ServiceActivationRequest.objects.select_for_update().select_related(
            "service",
            "country",
        ).filter(
            id=request_id
        ).first()

        if not request:
            return False, "Demande introuvable.", None

        if request.status != "validated":
            return False, "La demande doit etre validee avant activation.", request

        activation = ServiceActivation.objects.select_for_update().filter(
            service=request.service,
            country=request.country,
        ).first()

        if not activation:
            return False, "Relation service/pays introuvable.", request

        result = OperationalValidationService.validate_relation(
            request.service,
            request.country,
        )

        if not result.allowed:
            return False, result.message, request

        activation.active = True
        activation.validated_by_admin = True
        activation.reason = comment or "Activation validee par administration NSIKAY"
        activation.save(
            update_fields=[
                "active",
                "validated_by_admin",
                "reason",
            ]
        )

        request.status = "activated"
        request.admin_validated = True
        request.activated_at = timezone.now()
        request.validation_message = comment or "Activation effectuee."
        request.save(
            update_fields=[
                "status",
                "admin_validated",
                "activated_at",
                "validation_message",
                "updated_at",
            ]
        )

        ServiceDashboardLog.objects.create(
            action="activate",
            service=request.service,
            country=request.country,
            admin=admin_user,
            comment=comment or "Activation effectuee depuis une demande validee.",
        )

        return True, request.validation_message, request
