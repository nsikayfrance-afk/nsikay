from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
import json

from service_control.models import (
    GlobalService,
    CountryServiceStatus,
    ServiceActivation,
)

from .models import ServiceDashboardLog


def is_nsikay_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_nsikay_admin)
def activate_service(request, activation_id):

    activation = ServiceActivation.objects.select_related(
        "service",
        "country"
    ).filter(
        id=activation_id
    ).first()

    if not activation:
        messages.error(
            request,
            "Activation introuvable."
        )
        return redirect("service_dashboard:administration_statistics")

    activation.active = True
    activation.validated_by_admin = True
    activation.reason = (
        "Service active et valide par l'administration NSIKAY."
    )
    activation.save(
        update_fields=[
            "active",
            "validated_by_admin",
            "reason",
        ]
    )

    ServiceDashboardLog.objects.create(
        service=activation.service,
        country=activation.country,
        action="ACTIVATION",
        admin_user=request.user,
        comment=(
            "Activation du service "
            f"{activation.service.name} "
            f"pour {activation.country.country_name}."
        ),
    )

    messages.success(
        request,
        (
            f"Service « {activation.service.name} » "
            f"active pour {activation.country.country_name}."
        )
    )

    return redirect(
        "service_dashboard:administration_statistics"
    )


@user_passes_test(is_nsikay_admin)
def deactivate_service(request, activation_id):

    activation = ServiceActivation.objects.select_related(
        "service",
        "country"
    ).filter(
        id=activation_id
    ).first()

    if not activation:
        messages.error(
            request,
            "Activation introuvable."
        )
        return redirect("service_dashboard:administration_statistics")

    activation.active = False
    activation.reason = (
        "Service desactive par l'administration NSIKAY."
    )
    activation.save(
        update_fields=[
            "active",
            "reason",
        ]
    )

    ServiceDashboardLog.objects.create(
        service=activation.service,
        country=activation.country,
        action="DESACTIVATION",
        admin_user=request.user,
        comment=(
            "Desactivation du service "
            f"{activation.service.name} "
            f"pour {activation.country.country_name}."
        ),
    )

    messages.success(
        request,
        (
            f"Service « {activation.service.name} » "
            f"desactive pour {activation.country.country_name}."
        )
    )

    return redirect(
        "service_dashboard:administration_statistics"
    )


python manage.py check

