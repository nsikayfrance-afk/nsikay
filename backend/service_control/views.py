from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import (
    GlobalService,
    CountryServiceStatus,
)
from .management_helpers import (
    activate_country_service,
    deactivate_country_service,
)


@login_required
@require_GET
def service_country_status(request):
    service_name = request.GET.get("service")
    country_code = request.GET.get("country")

    if not service_name or not country_code:
        return JsonResponse(
            {
                "success": False,
                "message": "Les parametres service et country sont obligatoires.",
            },
            status=400,
        )

    service = GlobalService.objects.filter(
        name__iexact=service_name
    ).first()

    country = CountryServiceStatus.objects.filter(
        country_code__iexact=country_code
    ).first()

    if not service:
        return JsonResponse(
            {
                "success": False,
                "message": "Service NSIKAY introuvable.",
            },
            status=404,
        )

    if not country:
        return JsonResponse(
            {
                "success": False,
                "message": "Pays NSIKAY introuvable.",
            },
            status=404,
        )

    from .management_helpers import country_service_status

    result = country_service_status(service, country)

    return JsonResponse(
        {
            "success": True,
            "service": service.name,
            "category": service.category,
            "country": country.country_name,
            "country_code": country.country_code,
            **result,
        }
    )


@login_required
@require_POST
def activate_service_country(request):
    service_name = request.POST.get("service")
    country_code = request.POST.get("country")
    reason = request.POST.get("reason")

    if not service_name or not country_code:
        return JsonResponse(
            {
                "success": False,
                "message": "Les parametres service et country sont obligatoires.",
            },
            status=400,
        )

    service = GlobalService.objects.filter(
        name__iexact=service_name
    ).first()

    country = CountryServiceStatus.objects.filter(
        country_code__iexact=country_code
    ).first()

    if not service:
        return JsonResponse(
            {
                "success": False,
                "message": "Service NSIKAY introuvable.",
            },
            status=404,
        )

    if not country:
        return JsonResponse(
            {
                "success": False,
                "message": "Pays NSIKAY introuvable.",
            },
            status=404,
        )

    success, message, activation = activate_country_service(
        service,
        country,
        reason=reason,
    )

    return JsonResponse(
        {
            "success": success,
            "message": message,
            "service": service.name,
            "country": country.country_name,
            "country_code": country.country_code,
            "active": activation.active if activation else False,
            "validated_by_admin": (
                activation.validated_by_admin
                if activation
                else False
            ),
        },
        status=200 if success else 400,
    )


@login_required
@require_POST
def deactivate_service_country(request):
    service_name = request.POST.get("service")
    country_code = request.POST.get("country")
    reason = request.POST.get("reason")

    if not service_name or not country_code:
        return JsonResponse(
            {
                "success": False,
                "message": "Les parametres service et country sont obligatoires.",
            },
            status=400,
        )

    service = GlobalService.objects.filter(
        name__iexact=service_name
    ).first()

    country = CountryServiceStatus.objects.filter(
        country_code__iexact=country_code
    ).first()

    if not service:
        return JsonResponse(
            {
                "success": False,
                "message": "Service NSIKAY introuvable.",
            },
            status=404,
        )

    if not country:
        return JsonResponse(
            {
                "success": False,
                "message": "Pays NSIKAY introuvable.",
            },
            status=404,
        )

    success, message, activation = deactivate_country_service(
        service,
        country,
        reason=reason,
    )

    return JsonResponse(
        {
            "success": success,
            "message": message,
            "service": service.name,
            "country": country.country_name,
            "country_code": country.country_code,
            "active": activation.active if activation else False,
        },
        status=200 if success else 400,
    )

