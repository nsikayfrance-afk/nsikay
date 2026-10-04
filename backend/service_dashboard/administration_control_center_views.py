from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from service_control.models import (
    CountryServiceStatus,
    GlobalService,
    ServiceActivation,
)
from service_dashboard.models import (
    OperationalCountryConfigurationLog,
    ServiceDashboardLog,
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
def administration_control_center(request):

    primary_countries = CountryServiceStatus.objects.filter(
        is_primary=True
    )

    operational_countries = primary_countries.filter(
        is_operational=True
    )

    inactive_countries = primary_countries.filter(
        is_operational=False
    )

    services = GlobalService.objects.all().order_by("name")

    active_service_activations = ServiceActivation.objects.filter(
        active=True
    ).select_related("service", "country")

    inactive_service_activations = ServiceActivation.objects.filter(
        active=False
    ).select_related("service", "country")

    recent_service_logs = (
        ServiceDashboardLog.objects
        .select_related("service", "country")
        .order_by("-created_at")[:10]
    )

    configurations = (
        OperationalCountryConfigurationLog.objects
        .order_by("-created_at")[:10]
    )

    context = {
        "primary_count": primary_countries.count(),
        "operational_count": operational_countries.count(),
        "inactive_country_count": inactive_countries.count(),

        "service_count": services.count(),
        "global_active_service_count": services.filter(
            active_global=True
        ).count(),

        "active_activation_count": active_service_activations.count(),
        "inactive_activation_count": inactive_service_activations.count(),

        "recent_service_logs": recent_service_logs,
        "configurations": configurations,

        "operational_countries": operational_countries.order_by(
            "country_name"
        )[:20],

        "inactive_countries": inactive_countries.order_by(
            "country_name"
        )[:20],

        "services": services,
    }

    return render(
        request,
        "service_dashboard/administration_control_center.html",
        context,
    )

