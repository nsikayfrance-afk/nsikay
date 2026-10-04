from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db import models
from django.contrib import messages
import json
from django.core.paginator import Paginator
from django.db.models import Q
from service_control.models import GlobalService, CountryServiceStatus, ServiceActivation
from service_control.services import CountryServiceActivationManager
from .models import ServiceDashboardLog


def is_nsikay_admin(user):
    return user.is_authenticated and user.is_superuser


def dashboard_home(request):

    services = GlobalService.objects.count()
    countries = CountryServiceStatus.objects.count()
    activations_total = ServiceActivation.objects.count()
    activations_active = ServiceActivation.objects.filter(active=True).count()
    validations = ServiceActivation.objects.filter(
        validated_by_admin=True
    ).count()

    context = {
        "services": services,
        "countries": countries,
        "activations_total": activations_total,
        "activations_active": activations_active,
        "validations": validations,
    }

    return render(
        request,
        "service_dashboard/dashboard.html",
        context
    )


def administration_statistics(request):

    queryset = ServiceActivation.objects.select_related(
        "service",
        "country"
    ).order_by("-id")


    service = request.GET.get("service")
    country = request.GET.get("country")
    status = request.GET.get("status")
    validation = request.GET.get("validation")


    if service:
        queryset = queryset.filter(
            service__name__icontains=service
        )


    if country:
        queryset = queryset.filter(
            country__country_name__icontains=country
        )


    if status == "active":
        queryset = queryset.filter(
            active=True
        )

    elif status == "inactive":
        queryset = queryset.filter(
            active=False
        )


    if validation == "validated":
        queryset = queryset.filter(
            validated_by_admin=True
        )

    elif validation == "pending":
        queryset = queryset.filter(
            validated_by_admin=False
        )


    paginator = Paginator(
        queryset,
        50
    )


    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )


    context = {

        "activations": page_obj,

        "services_list": GlobalService.objects.all(),

        "countries_list": CountryServiceStatus.objects.all(),

    }


    return render(
        request,
        "service_dashboard/administration_statistics.html",
        context
    )

@user_passes_test(is_nsikay_admin)
def activate_service(request, activation_id):
    from django.shortcuts import redirect, get_object_or_404
    from django.contrib import messages

    activation = get_object_or_404(
        ServiceActivation.objects.select_related(
            "service",
            "country"
        ),
        id=activation_id
    )

    result = CountryServiceActivationManager.activate(
        activation.service,
        activation.country
    )

    if result.allowed:
        ServiceDashboardLog.objects.create(
            service=activation.service,
            country=activation.country,
            action="ACTIVATION",
            admin_user=str(request.user),
            comment=result.message
        )

        messages.success(
            request,
            result.message
        )
    else:
        messages.error(
            request,
            result.message
        )

    return redirect(
        "administration_statistics"
    )

@user_passes_test(is_nsikay_admin)
def deactivate_service(request, activation_id):
    from django.shortcuts import redirect, get_object_or_404
    from django.contrib import messages

    activation = get_object_or_404(
        ServiceActivation.objects.select_related(
            "service",
            "country"
        ),
        id=activation_id
    )

    result = CountryServiceActivationManager.deactivate(
        activation.service,
        activation.country,
        reason="Desactivation par administration NSIKAY."
    )

    if result.allowed:
        ServiceDashboardLog.objects.create(
            service=activation.service,
            country=activation.country,
            action="DESACTIVATION",
            admin_user=str(request.user),
            comment=result.message
        )

        messages.success(
            request,
            result.message
        )
    else:
        messages.error(
            request,
            result.message
        )

    return redirect(
        "administration_statistics"
    )

@user_passes_test(is_nsikay_admin)
def administration_history(request):
    logs = ServiceDashboardLog.objects.select_related(
        "service",
        "country"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "service_dashboard/administration_history.html",
        {
            "logs": logs
        }
    )

@user_passes_test(is_nsikay_admin)
def control_center(request):
    from django.shortcuts import render
    from service_control.models import (
        GlobalService,
        CountryServiceStatus,
        ServiceActivation,
        ServiceRule,
    )
    import json

    total = ServiceActivation.objects.count()

    actifs = ServiceActivation.objects.filter(
        active=True
    ).count()

    valides = ServiceActivation.objects.filter(
        validated_by_admin=True
    ).count()

    attente = ServiceActivation.objects.filter(
        validated_by_admin=False
    ).count()

    services_stats = list(
        ServiceActivation.objects
        .values("service__name")
        .annotate(
            total=models.Count("id"),
            actifs=models.Count(
                "id",
                filter=models.Q(active=True)
            )
        )
        .order_by("-actifs", "service__name")
    )

    pays_stats = list(
        ServiceActivation.objects
        .values("country_name")
        .annotate(
            total=models.Count("id"),
            actifs=models.Count(
                "id",
                filter=models.Q(active=True)
            )
        )
        .order_by("-actifs", "country_name")
    )

    service_chart_labels = [
        item["service__name"]
        for item in services_stats
    ]

    service_chart_values = [
        item["actifs"]
        for item in services_stats
    ]

    country_chart_labels = [
        item["country_name"]
        for item in pays_stats[:20]
    ]

    country_chart_values = [
        item["actifs"]
        for item in pays_stats[:20]
    ]

    activation_rate = 0

    if total > 0:
        activation_rate = round(
            (actifs / total) * 100,
            2
        )

    validation_rate = 0

    if total > 0:
        validation_rate = round(
            (valides / total) * 100,
            2
        )

    services_rules = []

    for service in GlobalService.objects.all().order_by("name"):
        try:
            rule = ServiceRule.objects.get(
                service=service
            )
        except ServiceRule.DoesNotExist:
            rule = None

        services_rules.append({
            "service": service,
            "rule": rule,
        })

    active_services = (
        ServiceActivation.objects
        .select_related("service", "country")
        .filter(active=True)
        .order_by("country_name", "service__name")
    )

    context = {
        "total": total,
        "actifs": actifs,
        "valides": valides,
        "attente": attente,
        "activation_rate": activation_rate,
        "validation_rate": validation_rate,
        "services_stats": services_stats,
        "pays_stats": pays_stats[:20],
        "service_chart_labels": json.dumps(
            service_chart_labels,
            ensure_ascii=False
        ),
        "service_chart_values": json.dumps(
            service_chart_values
        ),
        "country_chart_labels": json.dumps(
            country_chart_labels,
            ensure_ascii=False
        ),
        "country_chart_values": json.dumps(
            country_chart_values
        ),
        "services_rules": services_rules,
        "active_services": active_services,
    }

    return render(
        request,
        "service_dashboard/control_center.html",
        context
    )

def control_center_filtered(request):

    from service_control.models import ServiceActivation
    import json


    queryset = ServiceActivation.objects.all()


    service = request.GET.get("service")
    country = request.GET.get("country")
    status = request.GET.get("status")
    validation = request.GET.get("validation")


    if service:
        queryset = queryset.filter(
            service__id=service
        )


    if country:
        queryset = queryset.filter(
            country__id=country
        )


    if status == "active":
        queryset = queryset.filter(
            active=True
        )


    if status == "inactive":
        queryset = queryset.filter(
            active=False
        )


    if validation == "validated":
        queryset = queryset.filter(
            validated_by_admin=True
        )


    if validation == "pending":
        queryset = queryset.filter(
            validated_by_admin=False
        )


    total = queryset.count()

    actifs = queryset.filter(
        active=True
    ).count()


    valides = queryset.filter(
        validated_by_admin=True
    ).count()


    attente = queryset.filter(
        validated_by_admin=False
    ).count()



    services = queryset.values(
        "service__name"
    ).annotate(
        total=models.Count("id"),
        actifs=models.Count(
            "id",
            filter=models.Q(active=True)
        )
    )



    pays = queryset.values(
        "country_name"
    ).annotate(
        total=models.Count("id"),
        actifs=models.Count(
            "id",
            filter=models.Q(active=True)
        )
    )



    all_services = GlobalService.objects.all().order_by("name")

    all_countries = CountryServiceStatus.objects.values(
        "id",
        "country_name"
    ).distinct().order_by(
        "country_name"
    )


    return render(
        request,
        "service_dashboard/control_center.html",
        {
            "total": total,
            "actifs": actifs,
            "valides": valides,
            "attente": attente,

            "services_stats": services,
            "pays_stats": pays,

            "service_chart_labels": json.dumps(
                [x["service__name"] for x in services]
            ),

            "service_chart_values": json.dumps(
                [x["actifs"] for x in services]
            ),

            "country_chart_labels": json.dumps(
                [x["country__country_name"] for x in pays]
            ),

            "country_chart_values": json.dumps(
                [x["actifs"] for x in pays]
            ),
        }
    )






