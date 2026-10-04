from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from service_control.models import (
    CountryServiceStatus,
    GlobalService,
)

from banking.models import (
    Bank,
)

from partner_finance.models import (
    PartnerApplication,
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
                "Contrôleur Financier",
                "Banque Partenaire",
            ]
        ).exists()
    )


@user_passes_test(_is_nsikay_admin)
def financial_health_control(request):

    countries = CountryServiceStatus.objects.filter(
        is_primary=True
    ).order_by("country_name")

    services = GlobalService.objects.select_related(
        "rule"
    ).order_by("category", "name")

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

    country = None
    service = None

    if country_code:
        country = CountryServiceStatus.objects.filter(
            is_primary=True,
            country_code=country_code,
        ).first()

    if service_id.isdigit():
        service = GlobalService.objects.filter(
            id=int(service_id)
        ).select_related("rule").first()

    if request.method == "POST":

        if not country:
            messages.error(
                request,
                "Pays principal introuvable."
            )

        elif not service:
            messages.error(
                request,
                "Service introuvable."
            )

        else:

            rule = getattr(service, "rule", None)

            health_required = (
                rule.health_insurance_required
                if rule
                else False
            )

            bank_required = (
                rule.partner_bank_required
                if rule
                else False
            )

            financial_required = (
                rule.financial_partner_required
                if rule
                else False
            )

            banks = Bank.objects.filter(
                country__iexact=country.country_name,
                certified=True,
                active=True,
            )

            bank_available = banks.exists()

            financial_partner_available = (
                PartnerApplication.objects.filter(
                    status="approved",
                ).exists()
            )

            result = {
                "country": country,
                "service": service,
                "health_required": health_required,
                "bank_required": bank_required,
                "financial_required": financial_required,
                "bank_available": bank_available,
                "financial_partner_available": (
                    financial_partner_available
                ),
            }

            messages.info(
                request,
                "Contrôle assurance/partenaire effectué sans activation."
            )

    return render(
        request,
        "service_dashboard/financial_health_control.html",
        {
            "countries": countries,
            "services": services,
            "selected_country": country,
            "selected_service": service,
            "result": result,
        },
    )

