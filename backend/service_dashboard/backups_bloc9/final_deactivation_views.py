from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.http import HttpResponseNotAllowed

from service_control.models import ServiceActivation
from service_dashboard.models import ServiceDashboardLog


def _is_nsikay_admin(user):
    if not user or not user.is_authenticated:
        return False

    return (
        user.is_superuser
        or str(user.username).strip().lower()
        == "constantdoriskayembe"
        or user.groups.filter(
            name__in=[
                "Super Administrateur",
                "Administration Pays",
            ]
        ).exists()
    )


def final_deactivate_service(
    request,
    activation_id,
):

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    with transaction.atomic():

        activation = (
            ServiceActivation.objects
            .select_for_update()
            .select_related(
                "service",
                "country",
            )
            .get(
                id=activation_id,
            )
        )

        service = activation.service
        country = activation.country

        activation.active = False
        activation.reason = (
            "DÃƒÂ©sactivation effectuÃƒÂ©e par "
            "administration NSIKAY."
        )

        activation.save(
            update_fields=[
                "active",
                "reason",
            ]
        )

        ServiceDashboardLog.objects.create(
            action="deactivate",
            admin_user=(
                getattr(
                    request.user,
                    "username",
                    None,
                )
                or "Administration NSIKAY"
            ),
            comment=(
                f"DÃƒÂ©sactivation validÃƒÂ©e. "
                f"Service={service.name}; "
                f"Pays={country.country_name}"
            ),
            country=country,
            service=service,
        )

    messages.success(
        request,
        (
            f"Service {service.name} dÃƒÂ©sactivÃƒÂ© "
            f"pour {country.country_name}."
        ),
    )

    return redirect(
        "service_country_control"
    )

