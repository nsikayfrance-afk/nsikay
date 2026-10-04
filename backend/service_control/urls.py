from django.urls import path

from .views import (
    service_country_status,
    activate_service_country,
    deactivate_service_country,
)

urlpatterns = [
    path(
        "status/",
        service_country_status,
        name="service_country_status",
    ),
    path(
        "activate/",
        activate_service_country,
        name="activate_service_country",
    ),
    path(
        "deactivate/",
        deactivate_service_country,
        name="deactivate_service_country",
    ),
]

