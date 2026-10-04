from rest_framework.decorators import api_view
from rest_framework.response import Response

from service_control.models import (
    GlobalService,
    CountryServiceStatus,
    ServiceActivation
)

from service_dashboard.models import ServiceDashboardLog


@api_view(["GET"])
def service_matrix(request):

    data = []

    for service in GlobalService.objects.all():

        countries = []

        for activation in ServiceActivation.objects.filter(service=service):

            countries.append({

                "country": activation.country.country_name,
                "active": activation.active,
                "validated": activation.validated_by_admin

            })


        data.append({

            "service": service.name,
            "category": service.category,
            "countries": countries

        })


    return Response(data)



@api_view(["POST"])
def activate_service(request):

    service_id = request.data.get("service_id")
    country_id = request.data.get("country_id")

    service = GlobalService.objects.get(id=service_id)

    country = CountryServiceStatus.objects.get(id=country_id)


    activation, created = ServiceActivation.objects.get_or_create(
        service=service,
        country=country
    )


    activation.active = True
    activation.validated_by_admin = True
    activation.save()


    ServiceDashboardLog.objects.create(
        service=service,
        country=country,
        action="activate",
        admin_user="Administration NSIKAY"
    )


    return Response({

        "message":"Service active",
        "service":service.name,
        "country":country.country_name

    })



@api_view(["POST"])
def disable_service(request):

    service_id = request.data.get("service_id")
    country_id = request.data.get("country_id")

    service = GlobalService.objects.get(id=service_id)

    country = CountryServiceStatus.objects.get(id=country_id)


    activation = ServiceActivation.objects.get(
        service=service,
        country=country
    )


    activation.active = False
    activation.save()


    ServiceDashboardLog.objects.create(
        service=service,
        country=country,
        action="disable",
        admin_user="Administration NSIKAY"
    )


    return Response({

        "message":"Service desactive"

    })

