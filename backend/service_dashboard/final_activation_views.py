from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect

from service_control.models import ServiceActivation
from service_control.services import CountryServiceActivationValidator

from service_dashboard.models import ServiceDashboardLog


def _is_nsikay_admin(user):
    return bool(
        user
        and user.is_authenticated
        and user.is_superuser
    )


def final_activate_service(request, activation_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    if not _is_nsikay_admin(request.user):
        return HttpResponseNotAllowed(["POST"])

    with transaction.atomic():
        activation = get_object_or_404(
            ServiceActivation.objects.select_for_update().select_related(
                "service",
                "country",
            ),
            id=activation_id,
        )

        service = activation.service
        country = activation.country

        # Protection pays NSIKAY.
        if not country.is_primary:
            activation.active = False
            activation.validated_by_admin = False
            activation.reason = (
                "Activation refusee : pays non primaire dans la "
                "configuration NSIKAY."
            )
            activation.save(
                update_fields=[
                    "active",
                    "validated_by_admin",
                    "reason",
                ]
            )

            ServiceDashboardLog.objects.create(
                action="activate_refused",
                admin_user=request.user,
                comment=activation.reason,
                country=country,
                service=service,
            )

            return redirect("service_country_control")

        if not country.is_operational:
            activation.active = False
            activation.validated_by_admin = False
            activation.reason = (
                "Activation refusee : pays non operationnel."
            )
            activation.save(
                update_fields=[
                    "active",
                    "validated_by_admin",
                    "reason",
                ]
            )

            ServiceDashboardLog.objects.create(
                action="activate_refused",
                admin_user=request.user,
                comment=activation.reason,
                country=country,
                service=service,
            )

            return redirect("service_country_control")

        result = CountryServiceActivationValidator.validate(
            service,
            country,
        )

        allowed = bool(getattr(result, "allowed", False))
        message = getattr(result, "message", str(result))

        if not allowed:
            activation.active = False
            activation.validated_by_admin = False
            activation.reason = message
            activation.save(
                update_fields=[
                    "active",
                    "validated_by_admin",
                    "reason",
                ]
            )

            ServiceDashboardLog.objects.create(
                action="activate_refused",
                admin_user=request.user,
                comment=message,
                country=country,
                service=service,
            )

            return redirect("service_country_control")

        activation.active = True
        activation.validated_by_admin = True
        activation.reason = (
            "Activation finale validee par administration NSIKAY. "
            + message
        )

        activation.save(
            update_fields=[
                "active",
                "validated_by_admin",
                "reason",
            ]
        )

        ServiceDashboardLog.objects.create(
            action="activate",
            admin_user=request.user,
            comment=activation.reason,
            country=country,
            service=service,
        )

    return redirect("service_country_control")


def final_deactivate_service(request, activation_id):
    # POST uniquement : ce contrÃ´le doit Ãªtre le premier.
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # Administration NSIKAY uniquement.
    if not _is_nsikay_admin(request.user):
        return HttpResponseNotAllowed(["POST"])


    with transaction.atomic():
        activation = get_object_or_404(
            ServiceActivation.objects.select_for_update().select_related(
                "service",
                "country",
            ),
            id=activation_id,
        )

        activation.active = False
        activation.validated_by_admin = False
        activation.reason = (
            "Desactivation finale effectuee par administration NSIKAY."
        )

        activation.save(
            update_fields=[
                "active",
                "validated_by_admin",
                "reason",
            ]
        )

        ServiceDashboardLog.objects.create(
            action="deactivate",
            admin_user=request.user,
            comment=activation.reason,
            country=activation.country,
            service=activation.service,
        )

    return redirect("service_country_control")
