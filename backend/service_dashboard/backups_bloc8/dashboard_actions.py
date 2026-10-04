from django.shortcuts import redirect, get_object_or_404
from service_control.models import ServiceActivation
from .models import ServiceDashboardLog


def activate_service(request, activation_id):

    activation = get_object_or_404(
        ServiceActivation,
        id=activation_id
    )

    activation.active = True
    activation.validated_by_admin = True
    activation.save()


    ServiceDashboardLog.objects.create(

        action="ACTIVATION",

        service_name=activation.service.name,

        country_name=activation.country.country_name,

        user=request.user.username,

        message="Service activé par administration NSIKAY"

    )


    return redirect(
        "administration_statistics"
    )



def deactivate_service(request, activation_id):

    activation = get_object_or_404(
        ServiceActivation,
        id=activation_id
    )

    activation.active = False
    activation.save()


    ServiceDashboardLog.objects.create(

        action="DESACTIVATION",

        service_name=activation.service.name,

        country_name=activation.country.country_name,

        user=request.user.username,

        message="Service désactivé par administration NSIKAY"

    )


    return redirect(
        "administration_statistics"
    )
