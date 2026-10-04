from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from service_control.models import (
    CountryServiceStatus,
    GlobalService,
    ServiceActivation,
    ServiceRule,
)


def _is_nsikay_admin(user):
    if not user or not user.is_authenticated:
        return False

    username = str(user.username).strip().lower()

    if username == "constantdoriskayembe":
        return True

    return (
        user.is_superuser
        or user.groups.filter(
            name__in=[
                "Super Administrateur",
                "Administration Pays",
            ]
        ).exists()
    )


@user_passes_test(_is_nsikay_admin)
def service_country_control(request):

    countries = list(
        CountryServiceStatus.objects
        .filter(is_primary=True)
        .order_by("country_name")
    )

    services = list(
        GlobalService.objects
        .select_related("rule")
        .order_by("category", "name")
    )

    # -----------------------------------------------------
    # FILTRES
    # -----------------------------------------------------

    country_code = (
        request.GET.get("country")
        or ""
    ).strip().upper()

    service_id = (
        request.GET.get("service")
        or ""
    ).strip()

    selected_country = None
    selected_service = None

    if country_code:
        selected_country = (
            CountryServiceStatus.objects
            .filter(
                is_primary=True,
                country_code=country_code,
            )
            .first()
        )

    if service_id.isdigit():
        selected_service = (
            GlobalService.objects
            .select_related("rule")
            .filter(id=int(service_id))
            .first()
        )

    # -----------------------------------------------------
    # MATRICE FILTREE
    # -----------------------------------------------------

    rows = []

    if selected_country and selected_service:

        activation = (
            ServiceActivation.objects
            .filter(
                country=selected_country,
                service=selected_service,
            )
            .first()
        )

        rule = (
            ServiceRule.objects
            .filter(service=selected_service)
            .first()
        )

        rows.append({
            "country": selected_country,
            "service": selected_service,
            "activation": activation,
            "rule": rule,
        })

    elif selected_country:

        activations = {
            item.service_id: item
            for item in ServiceActivation.objects
            .filter(
                country=selected_country,
            )
            .select_related("service")
        }

        for service in services:

            rows.append({
                "country": selected_country,
                "service": service,
                "activation": activations.get(service.id),
                "rule": getattr(service, "rule", None),
            })

    elif selected_service:

        activations = {
            item.country_id: item
            for item in ServiceActivation.objects
            .filter(
                service=selected_service,
            ).select_related("country")
        }

        for country in countries:

            rows.append({
                "country": country,
                "service": selected_service,
                "activation": activations.get(country.id),
                "rule": getattr(selected_service, "rule", None),
            })

    # -----------------------------------------------------
    # STATISTIQUES
    # -----------------------------------------------------

    operational_count = (
        CountryServiceStatus.objects
        .filter(
            is_primary=True,
            is_operational=True,
        )
        .count()
    )

    active_count = (
        ServiceActivation.objects
        .filter(active=True)
        .count()
    )

    validated_count = (
        ServiceActivation.objects
        .filter(validated_by_admin=True)
        .count()
    )

    return render(
        request,
        "service_dashboard/service_country_control.html",
        {
            "countries": countries,
            "services": services,
            "rows": rows,
            "selected_country": selected_country,
            "selected_service": selected_service,
            "operational_count": operational_count,
            "active_count": active_count,
            "validated_count": validated_count,
            "total_relations": ServiceActivation.objects.count(),
        },
    )
