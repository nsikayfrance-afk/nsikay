from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from .models import (
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
def global_administrative_log(request):

    country_logs = list(
        OperationalCountryConfigurationLog.objects
        .all()
        .order_by("-created_at")[:100]
    )

    service_logs = list(
        ServiceDashboardLog.objects
        .select_related("country", "service")
        .all()
        .order_by("-created_at")[:100]
    )

    entries = []

    for log in country_logs:
        entries.append({
            "date": log.created_at,
            "type": "Configuration pays",
            "action": log.action,
            "administrateur": (
                log.admin_user
                or "Administration NSIKAY"
            ),
            "service": "—",
            "pays": "Configuration mondiale",
            "details": (
                f"{log.selected_count} pays sélectionnés"
            ),
            "statut": (
                "ANNULÉE"
                if getattr(log, "rolled_back", False)
                else "ACTIVE"
            ),
        })

    for log in service_logs:
        entries.append({
            "date": log.created_at,
            "type": "Service",
            "action": log.action,
            "administrateur": (
                log.admin_user
                or "Administration NSIKAY"
            ),
            "service": str(log.service),
            "pays": str(log.country),
            "details": log.comment or "Aucun commentaire",
            "statut": "ENREGISTRÉ",
        })

    entries.sort(
        key=lambda item: item["date"],
        reverse=True,
    )

    entries = entries[:200]

    return render(
        request,
        "service_dashboard/global_administrative_log.html",
        {
            "entries": entries,
            "country_log_count": len(country_logs),
            "service_log_count": len(service_logs),
            "total_entries": len(entries),
        },
    )

