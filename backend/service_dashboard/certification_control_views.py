from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from service_control.models import (
    CountryServiceStatus,
    GlobalService,
)


def _is_nsikay_admin(user):
    if not user or not user.is_authenticated:
        return False

    return (
        user.is_superuser
        or str(user.username).strip().lower() == "constantdoriskayembe"
        or user.groups.filter(
            name__in=[
                "Super Administrateur",
                "Administration Pays",
                "Autorité Certification",
            ]
        ).exists()
    )


@user_passes_test(_is_nsikay_admin)
def certification_control(request):

    countries = CountryServiceStatus.objects.filter(
        is_primary=True
    ).order_by("country_name")

    services = GlobalService.objects.select_related(
        "rule"
    ).order_by("category", "name")

    selected_country = None
    selected_service = None
    result = None

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
        selected_country = CountryServiceStatus.objects.filter(
            is_primary=True,
            country_code=country_code,
        ).first()

    if service_id.isdigit():
        selected_service = GlobalService.objects.filter(
            id=int(service_id)
        ).select_related("rule").first()

    if request.method == "POST":

        if not selected_country:
            messages.error(
                request,
                "Pays principal introuvable."
            )

        elif not selected_service:
            messages.error(
                request,
                "Service introuvable."
            )

        else:

            rule = getattr(
                selected_service,
                "rule",
                None,
            )

            certification_required = (
                rule.certification_required
                if rule
                else True
            )

            result = {
                "country": selected_country,
                "service": selected_service,
                "required": certification_required,
                "status": (
                    "CERTIFICATION_REQUISE"
                    if certification_required
                    else "CERTIFICATION_NON_REQUISE"
                ),
            }

            messages.info(
                request,
                "Contrôle de la règle de certification effectué."
            )

    return render(
        request,
        "service_dashboard/certification_control.html",
        {
            "countries": countries,
            "services": services,
            "selected_country": selected_country,
            "selected_service": selected_service,
            "result": result,
        },
    )

