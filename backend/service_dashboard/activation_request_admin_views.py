from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from service_dashboard.models import ServiceActivationRequest


def _is_nsikay_admin(user):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    allowed_groups = {
        "Super Administrateur",
        "Administration Pays",
        "Administration NSIKAY",
        "Administrateur NSIKAY",
    }

    return user.groups.filter(name__in=allowed_groups).exists()


@login_required
def activation_request_admin_list(request):
    """
    Interface principale d'administration des demandes.

    IMPORTANT :
    Cette vue ne déclenche aucune activation.
    """

    if not _is_nsikay_admin(request.user):
        return render(
            request,
            "service_dashboard/access_denied.html",
            {
                "message": "Accès réservé à l'administration NSIKAY."
            },
            status=403,
        )

    queryset = (
        ServiceActivationRequest.objects
        .select_related(
            "service",
            "country",
            "requested_by",
        )
        .order_by("-created_at")
    )

    status_filter = request.GET.get("status", "").strip()
    country_filter = request.GET.get("country", "").strip()
    service_filter = request.GET.get("service", "").strip()
    search = request.GET.get("q", "").strip()

    if status_filter:
        queryset = queryset.filter(status=status_filter)

    if country_filter:
        queryset = queryset.filter(country__country_name__iexact=country_filter)

    if service_filter:
        queryset = queryset.filter(service__name__iexact=service_filter)

    if search:
        queryset = queryset.filter(
            service__name__icontains=search
        ) | queryset.filter(
            country__country_name__icontains=search
        ) | queryset.filter(
            requested_by__username__icontains=search
        )

    paginator = Paginator(queryset.distinct(), 25)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    countries = (
        ServiceActivationRequest.objects
        .select_related("country")
        .values_list("country__country_name", flat=True)
        .distinct()
        .order_by("country__country_name")
    )

    services = (
        ServiceActivationRequest.objects
        .select_related("service")
        .values_list("service__name", flat=True)
        .distinct()
        .order_by("service__name")
    )

    context = {
        "page_obj": page_obj,
        "requests": page_obj.object_list,
        "countries": countries,
        "services": services,
        "status_filter": status_filter,
        "country_filter": country_filter,
        "service_filter": service_filter,
        "search": search,
        "total_requests": ServiceActivationRequest.objects.count(),
        "pending_count": ServiceActivationRequest.objects.filter(
            status="pending"
        ).count(),
        "approved_count": ServiceActivationRequest.objects.filter(
            status="approved"
        ).count(),
        "rejected_count": ServiceActivationRequest.objects.filter(
            status="rejected"
        ).count(),
        "expired_count": ServiceActivationRequest.objects.filter(
            status="expired"
        ).count(),
    }

    return render(
        request,
        "service_dashboard/activation_request_admin_list.html",
        context,
    )


@login_required
def activation_request_admin_history(request):
    """
    Historique administratif des demandes déjà traitées.

    Ne modifie aucune donnée.
    Ne déclenche aucune activation.
    """

    if not _is_nsikay_admin(request.user):
        return render(
            request,
            "service_dashboard/access_denied.html",
            {
                "message": "Accès réservé à l'administration NSIKAY."
            },
            status=403,
        )

    queryset = (
        ServiceActivationRequest.objects
        .select_related(
            "service",
            "country",
            "requested_by",
        )
        .filter(status__in=["approved", "rejected", "expired"])
        .order_by("-updated_at", "-created_at")
    )

    paginator = Paginator(queryset, 25)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(
        request,
        "service_dashboard/activation_request_admin_history.html",
        {
            "page_obj": page_obj,
            "requests": page_obj.object_list,
            "total_history": queryset.count(),
        },
    )


@login_required
def activation_request_admin_detail(request, request_id):
    """
    Fiche détaillée d'une demande.

    Cette vue est strictement informative.
    """

    if not _is_nsikay_admin(request.user):
        return render(
            request,
            "service_dashboard/access_denied.html",
            {
                "message": "Accès réservé à l'administration NSIKAY."
            },
            status=403,
        )

    activation_request = get_object_or_404(
        ServiceActivationRequest.objects.select_related(
            "service",
            "country",
            "requested_by",
        ),
        pk=request_id,
    )

    return render(
        request,
        "service_dashboard/activation_request_admin_detail.html",
        {
            "activation_request": activation_request,
        },
    )

