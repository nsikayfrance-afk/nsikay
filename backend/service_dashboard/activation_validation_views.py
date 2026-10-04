from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.shortcuts import redirect, render

from service_control.models import (
    CountryServiceStatus,
    GlobalService,
    ServiceActivation,
)

from service_control.services import (
    CountryServiceActivationValidator,
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


def _validate_service_country(service, country):
    """
    Point central de validation.

    Aucune modification de ServiceActivation n'est effectuée ici.
    """

    try:
        result = CountryServiceActivationValidator.validate(
            service,
            country,
        )

        if isinstance(result, tuple):
            valid, reason = result
        else:
            valid = bool(result)
            reason = (
                "Validation réussie."
                if valid
                else "Validation refusée."
            )

        return bool(valid), str(reason)

    except Exception as exc:
        return (
            False,
            f"Erreur de validation : {exc}",
        )


@user_passes_test(_is_nsikay_admin)
def activation_validation(request):

    countries = (
        CountryServiceStatus.objects
        .filter(is_primary=True)
        .order_by("country_name")
    )

    services = (
        GlobalService.objects
        .select_related("rule")
        .order_by("category", "name")
    )

    result = None
    selected_country = None
    selected_service = None

    country_code = (
        request.GET.get("country")
        or request.POST.get("country")
        or ""
    ).strip().upper()

    service_id = (
        request.GET.get("service")
        or request.POST.get("service")
        or ""
    ).strip()

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
            .filter(id=int(service_id))
            .select_related("rule")
            .first()
        )

    if request.method == "POST":

        if not selected_country:
            messages.error(
                request,
                "Pays introuvable ou non principal.",
            )

        elif not selected_service:
            messages.error(
                request,
                "Service introuvable.",
            )

        else:

            valid, reason = _validate_service_country(
                selected_service,
                selected_country,
            )

            result = {
                "valid": valid,
                "reason": reason,
                "country": selected_country,
                "service": selected_service,
            }

            if valid:
                messages.success(
                    request,
                    (
                        "Toutes les conditions actuelles de validation "
                        "sont satisfaites. Aucune activation n'a été "
                        "effectuée."
                    ),
                )
            else:
                messages.warning(
                    request,
                    (
                        "Activation refusée par le contrôle préalable : "
                        f"{reason}"
                    ),
                )

    elif selected_country and selected_service:

        valid, reason = _validate_service_country(
            selected_service,
            selected_country,
        )

        result = {
            "valid": valid,
            "reason": reason,
            "country": selected_country,
            "service": selected_service,
        }

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
        "service_dashboard/activation_validation.html",
        {
            "countries": countries,
            "services": services,
            "selected_country": selected_country,
            "selected_service": selected_service,
            "result": result,
            "active_count": active_count,
            "validated_count": validated_count,
            "total_relations": ServiceActivation.objects.count(),
        },
    )

