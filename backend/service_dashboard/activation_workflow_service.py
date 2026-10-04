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
class WorkflowResult:
    allowed: bool
    message: str
    request: object = None
    activation: object = None
    service: object = None
    country: object = None


class ActivationWorkflowService:

    @staticmethod
    def _load(service_id, country_id):

        service = GlobalService.objects.filter(
            id=service_id
        ).first()

        country = CountryServiceStatus.objects.filter(
            id=country_id
        ).first()

        if not service:
            return WorkflowResult(
                False,
                "Service introuvable.",
            )

        if not country:
            return WorkflowResult(
                False,
                "Pays introuvable.",
                service=service,
            )

        return WorkflowResult(
            True,
            "Chargement effectue.",
            service=service,
            country=country,
        )

    @staticmethod
    def check_country(service, country):

        activation = ServiceActivation.objects.filter(
            service=service,
            country=country,
        ).first()

        if not activation:
            return WorkflowResult(
                False,
                "Aucune relation service/pays.",
                service=service,
                country=country,
            )

        if not country.is_primary:
            return WorkflowResult(
                False,
                "Le pays n'est pas un pays primaire NSIKAY.",
                service=service,
                country=country,
                activation=activation,
            )

        if not country.is_operational:
            return WorkflowResult(
                False,
                "Le pays n'est pas operationnel.",
                service=service,
                country=country,
                activation=activation,
            )

        return WorkflowResult(
            True,
            "Pays autorise.",
            service=service,
            country=country,
            activation=activation,
        )

    @staticmethod
    def check_rule(service, country):

        result = ActivationWorkflowService.check_country(
            service,
            country,
        )

        if not result.allowed:
            return result

        rule = ServiceRule.objects.filter(
            service=service
        ).first()

        if not rule:
            return WorkflowResult(
                False,
                "Aucune regle configuree pour ce service.",
                service=service,
                country=country,
                activation=result.activation,
            )

        return WorkflowResult(
            True,
            "Regle de service disponible.",
            service=service,
            country=country,
            activation=result.activation,
        )

    @staticmethod
    def precheck_request(request):

        if not request:
            return WorkflowResult(
                False,
                "Demande inexistante.",
            )

        result = ActivationWorkflowService.check_rule(
            request.service,
            request.country,
        )

        result.request = request

        if not result.allowed:
            return result

        return WorkflowResult(
            True,
            "Precontrole de la demande reussi.",
            request=request,
            activation=result.activation,
            service=request.service,
            country=request.country,
        )

    @staticmethod
    @transaction.atomic
    def create_request(
        service,
        country,
        requested_by,
        beneficiary_user=None,
        reason="",
    ):

        beneficiary_user = beneficiary_user or requested_by

        existing = ServiceActivationRequest.objects.select_for_update().filter(
            service=service,
            country=country,
            beneficiary_user=beneficiary_user,
            status="pending",
        ).first()

        if existing:
            return WorkflowResult(
                False,
                "Une demande identique est deja en attente.",
                request=existing,
                service=service,
                country=country,
            )

        result = ActivationWorkflowService.check_rule(
            service,
            country,
        )

        if not result.allowed:
            return WorkflowResult(
                False,
                result.message,
                service=service,
                country=country,
                activation=result.activation,
            )

        request = ServiceActivationRequest.objects.create(
            service=service,
            country=country,
            requested_by=requested_by,
            beneficiary_user=beneficiary_user,
            status="pending",
            certification_checked=False,
            health_insurance_checked=False,
            bank_partner_checked=False,
            financial_partner_checked=False,
            country_authorization_checked=True,
            admin_validated=False,
            validation_message=reason or "Demande creee.",
            rejection_reason="",
        )

        ServiceDashboardLog.objects.create(
            action="request",
            service=service,
            country=country,
            admin=requested_by,
            comment=reason or "Demande d'activation creee.",
        )

        return WorkflowResult(
            True,
            "Demande d'activation creee.",
            request=request,
            activation=result.activation,
            service=service,
            country=country,
        )

    @staticmethod
    @transaction.atomic
    def validate_request(request, admin_user, message=""):

        locked = ServiceActivationRequest.objects.select_for_update().select_related(
            "service",
            "country",
            "requested_by",
            "beneficiary_user",
        ).filter(
            id=request.id
        ).first()

        if not locked:
            return WorkflowResult(
                False,
                "Demande introuvable.",
            )

        if locked.status != "pending":
            return WorkflowResult(
                False,
                "Seule une demande en attente peut etre validee.",
                request=locked,
                service=locked.service,
                country=locked.country,
            )

        result = ActivationWorkflowService.check_rule(
            locked.service,
            locked.country,
        )

        if not result.allowed:

            locked.status = "rejected"
            locked.admin_validated = False
            locked.rejection_reason = result.message
            locked.validation_message = result.message
            locked.validated_at = timezone.now()

            locked.save(
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
                service=locked.service,
                country=locked.country,
                admin=admin_user,
                comment=result.message,
            )

            return WorkflowResult(
                False,
                result.message,
                request=locked,
                service=locked.service,
                country=locked.country,
                activation=result.activation,
            )

        locked.status = "validated"
        locked.admin_validated = True
        locked.validation_message = (
            message or
            "Demande validee par administration NSIKAY."
        )
        locked.rejection_reason = ""
        locked.validated_at = timezone.now()

        locked.save(
            update_fields=[
                "status",
                "admin_validated",
                "validation_message",
                "rejection_reason",
                "validated_at",
                "updated_at",
            ]
        )

        ServiceDashboardLog.objects.create(
            action="validate",
            service=locked.service,
            country=locked.country,
            admin=admin_user,
            comment=locked.validation_message,
        )

        return WorkflowResult(
            True,
            locked.validation_message,
            request=locked,
            service=locked.service,
            country=locked.country,
            activation=result.activation,
        )

    @staticmethod
    @transaction.atomic
    def activate_validated(request, admin_user, message=""):

        locked_request = ServiceActivationRequest.objects.select_for_update().select_related(
            "service",
            "country",
        ).filter(
            id=request.id
        ).first()

        if not locked_request:
            return WorkflowResult(
                False,
                "Demande introuvable.",
            )

        if locked_request.status != "validated":
            return WorkflowResult(
                False,
                "La demande doit etre validee avant activation.",
                request=locked_request,
                service=locked_request.service,
                country=locked_request.country,
            )

        result = ActivationWorkflowService.check_rule(
            locked_request.service,
            locked_request.country,
        )

        if not result.allowed:
            return WorkflowResult(
                False,
                result.message,
                request=locked_request,
                service=locked_request.service,
                country=locked_request.country,
                activation=result.activation,
            )

        activation = ServiceActivation.objects.select_for_update().filter(
            service=locked_request.service,
            country=locked_request.country,
        ).first()

        if not activation:
            return WorkflowResult(
                False,
                "Relation service/pays introuvable.",
                request=locked_request,
                service=locked_request.service,
                country=locked_request.country,
            )

        if activation.active:
            return WorkflowResult(
                False,
                "Le service est deja actif dans ce pays.",
                request=locked_request,
                activation=activation,
                service=locked_request.service,
                country=locked_request.country,
            )

        activation.active = True
        activation.validated_by_admin = True
        activation.reason = (
            message or
            "Activation finale validee par administration NSIKAY."
        )

        activation.save(
            update_fields=[
                "active",
                "validated_by_admin",
                "reason",
            ]
        )

        locked_request.status = "activated"
        locked_request.admin_validated = True
        locked_request.activated_at = timezone.now()
        locked_request.validation_message = (
            message or
            "Activation finale executee."
        )

        locked_request.save(
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
            service=locked_request.service,
            country=locked_request.country,
            admin=admin_user,
            comment=locked_request.validation_message,
        )

        return WorkflowResult(
            True,
            locked_request.validation_message,
            request=locked_request,
            activation=activation,
            service=locked_request.service,
            country=locked_request.country,
        )

    @staticmethod
    @transaction.atomic
    def reject_request(request, admin_user, reason):

        locked = ServiceActivationRequest.objects.select_for_update().filter(
            id=request.id
        ).first()

        if not locked:
            return WorkflowResult(
                False,
                "Demande introuvable.",
            )

        if locked.status != "pending":
            return WorkflowResult(
                False,
                "Seule une demande en attente peut etre rejetee.",
                request=locked,
            )

        locked.status = "rejected"
        locked.admin_validated = False
        locked.rejection_reason = reason
        locked.validation_message = reason
        locked.validated_at = timezone.now()

        locked.save(
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
            service=locked.service,
            country=locked.country,
            admin=admin_user,
            comment=reason,
        )

        return WorkflowResult(
            True,
            reason,
            request=locked,
        )
