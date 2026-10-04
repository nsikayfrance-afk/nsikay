from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from service_control.models import (
    GlobalService,
    CountryServiceStatus,
)

from service_dashboard.models import (
    ServiceActivationRequest,
)

from service_dashboard.activation_workflow_service import (
    ActivationWorkflowService,
)


def _is_nsikay_admin(user):
    return bool(
        user
        and user.is_authenticated
        and user.is_superuser
    )


def _admin_required(request):
    return _is_nsikay_admin(request.user)


@login_required
@require_http_methods(["GET"])
def workflow_dashboard(request):

    if not _admin_required(request):
        return render(
            request,
            "service_dashboard/workflow_forbidden.html",
            status=403,
        )

    status = request.GET.get("status", "").strip()
    service_id = request.GET.get("service", "").strip()
    country_id = request.GET.get("country", "").strip()

    requests_qs = ServiceActivationRequest.objects.select_related(
        "service",
        "country",
        "requested_by",
        "beneficiary_user",
    ).order_by(
        "-created_at"
    )

    if status:
        requests_qs = requests_qs.filter(
            status=status
        )

    if service_id:
        requests_qs = requests_qs.filter(
            service_id=service_id
        )

    if country_id:
        requests_qs = requests_qs.filter(
            country_id=country_id
        )

    context = {
        "requests": requests_qs,
        "services": GlobalService.objects.order_by("name"),
        "countries": CountryServiceStatus.objects.filter(
            is_primary=True
        ).order_by("country_name"),
        "selected_status": status,
        "selected_service": service_id,
        "selected_country": country_id,
        "status_choices": ServiceActivationRequest.STATUS_CHOICES,
    }

    return render(
        request,
        "service_dashboard/workflow_dashboard.html",
        context,
    )


@login_required
@require_http_methods(["GET", "POST"])
def workflow_create_request(request):

    if not _admin_required(request):
        return render(
            request,
            "service_dashboard/workflow_forbidden.html",
            status=403,
        )

    services = GlobalService.objects.order_by("name")

    countries = CountryServiceStatus.objects.filter(
        is_primary=True,
        is_operational=True,
    ).order_by("country_name")

    if request.method == "GET":
        return render(
            request,
            "service_dashboard/workflow_create_request.html",
            {
                "services": services,
                "countries": countries,
            },
        )

    service_id = request.POST.get("service_id", "").strip()
    country_id = request.POST.get("country_id", "").strip()
    reason = request.POST.get("reason", "").strip()

    if not service_id or not country_id:
        messages.error(
            request,
            "Le service et le pays sont obligatoires.",
        )

        return render(
            request,
            "service_dashboard/workflow_create_request.html",
            {
                "services": services,
                "countries": countries,
            },
            status=400,
        )

    service = get_object_or_404(
        GlobalService,
        id=service_id,
    )

    country = get_object_or_404(
        CountryServiceStatus,
        id=country_id,
        is_primary=True,
        is_operational=True,
    )

    result = ActivationWorkflowService.create_request(
        service=service,
        country=country,
        requested_by=request.user,
        beneficiary_user=request.user,
        reason=reason,
    )

    if not result.allowed:
        messages.error(
            request,
            result.message,
        )

        return render(
            request,
            "service_dashboard/workflow_create_request.html",
            {
                "services": services,
                "countries": countries,
            },
            status=400,
        )

    messages.success(
        request,
        result.message,
    )

    return redirect(
        "workflow_admin_detail",
        request_id=result.request.id,
    )


@login_required
@require_http_methods(["GET"])
def workflow_detail(request, request_id):

    if not _admin_required(request):
        return render(
            request,
            "service_dashboard/workflow_forbidden.html",
            status=403,
        )

    activation_request = get_object_or_404(
        ServiceActivationRequest.objects.select_related(
            "service",
            "country",
            "requested_by",
            "beneficiary_user",
        ),
        id=request_id,
    )

    return render(
        request,
        "service_dashboard/workflow_detail.html",
        {
            "activation_request": activation_request,
        },
    )


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def workflow_validate(request, request_id):

    if not _admin_required(request):
        return HttpResponseNotAllowed(["POST"])

    activation_request = get_object_or_404(
        ServiceActivationRequest,
        id=request_id,
    )

    message = request.POST.get(
        "message",
        "",
    ).strip()

    result = ActivationWorkflowService.validate_request(
        activation_request,
        request.user,
        message=message,
    )

    if result.allowed:
        messages.success(
            request,
            result.message,
        )
    else:
        messages.error(
            request,
            result.message,
        )

    return redirect(
        "workflow_admin_detail",
        request_id=request_id,
    )


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def workflow_reject(request, request_id):

    if not _admin_required(request):
        return HttpResponseNotAllowed(["POST"])

    activation_request = get_object_or_404(
        ServiceActivationRequest,
        id=request_id,
    )

    reason = request.POST.get(
        "reason",
        "",
    ).strip()

    if not reason:
        messages.error(
            request,
            "Le motif du rejet est obligatoire.",
        )

        return redirect(
            "workflow_admin_detail",
            request_id=request_id,
        )

    result = ActivationWorkflowService.reject_request(
        activation_request,
        request.user,
        reason,
    )

    if result.allowed:
        messages.success(
            request,
            "Demande rejetee et journalisee.",
        )
    else:
        messages.error(
            request,
            result.message,
        )

    return redirect(
        "workflow_admin_detail",
        request_id=request_id,
    )


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def workflow_activate(request, request_id):

    if not _admin_required(request):
        return HttpResponseNotAllowed(["POST"])

    activation_request = get_object_or_404(
        ServiceActivationRequest,
        id=request_id,
    )

    message = request.POST.get(
        "message",
        "",
    ).strip()

    result = ActivationWorkflowService.activate_validated(
        activation_request,
        request.user,
        message=message,
    )

    if result.allowed:
        messages.success(
            request,
            "Activation finale executee.",
        )
    else:
        messages.error(
            request,
            result.message,
        )

    return redirect(
        "workflow_admin_detail",
        request_id=request_id,
    )
