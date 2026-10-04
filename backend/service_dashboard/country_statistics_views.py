from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from service_control.models import CountryServiceStatus
from service_dashboard.models import OperationalCountryConfigurationLog


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
def country_statistics(request):
    primary_count = CountryServiceStatus.objects.filter(
        is_primary=True
    ).count()

    operational_count = CountryServiceStatus.objects.filter(
        is_primary=True,
        is_operational=True,
    ).count()

    inactive_count = primary_count - operational_count

    operational_percent = (
        round((operational_count / primary_count) * 100, 2)
        if primary_count
        else 0
    )

    last_configuration = (
        OperationalCountryConfigurationLog.objects
        .order_by("-created_at")
        .first()
    )

    configuration_count = (
        OperationalCountryConfigurationLog.objects.count()
    )

    rolled_back_count = (
        OperationalCountryConfigurationLog.objects
        .filter(rolled_back=True)
        .count()
    )

    context = {
        "primary_count": primary_count,
        "operational_count": operational_count,
        "inactive_count": inactive_count,
        "operational_percent": operational_percent,
        "last_configuration": last_configuration,
        "configuration_count": configuration_count,
        "rolled_back_count": rolled_back_count,
    }

    return render(
        request,
        "service_dashboard/country_statistics.html",
        context,
    )

