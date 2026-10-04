from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Count

from service_control.models import (
    GlobalService,
    CountryServiceStatus,
    ServiceActivation
)

from service_dashboard.models import ServiceDashboardLog


@api_view(["GET"])
def administration_statistics(request):

    total_services = GlobalService.objects.count()

    total_countries = CountryServiceStatus.objects.count()

    total_matrix = ServiceActivation.objects.count()

    active_services = ServiceActivation.objects.filter(
        active=True
    ).count()

    validated_services = ServiceActivation.objects.filter(
        validated_by_admin=True
    ).count()

    waiting_services = ServiceActivation.objects.filter(
        active=False,
        validated_by_admin=False
    ).count()


    services = []

    for service in GlobalService.objects.all():

        total = ServiceActivation.objects.filter(
            service=service
        ).count()

        active = ServiceActivation.objects.filter(
            service=service,
            active=True
        ).count()


        services.append({

            "service": service.name,

            "total_pays": total,

            "actifs": active,

            "inactifs": total-active

        })


    countries = []

    for country in CountryServiceStatus.objects.all():

        total = ServiceActivation.objects.filter(
            country=country
        ).count()

        active = ServiceActivation.objects.filter(
            country=country,
            active=True
        ).count()


        countries.append({

            "pays": country.country_name,

            "services": total,

            "actifs": active

        })


    return Response({

        "statistiques_globales": {

            "services": total_services,

            "pays": total_countries,

            "matrice": total_matrix,

            "actifs": active_services,

            "valides": validated_services,

            "attente": waiting_services

        },

        "par_service": services,

        "par_pays": countries,

        "logs_total": ServiceDashboardLog.objects.count()

    })

