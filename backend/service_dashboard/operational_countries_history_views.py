from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from service_dashboard.models import (
    OperationalCountryConfigurationLog
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
def operational_countries_history(request):

    logs = (
        OperationalCountryConfigurationLog.objects
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "service_dashboard/operational_countries_history.html",
        {
            "logs": logs,
        }
    )

