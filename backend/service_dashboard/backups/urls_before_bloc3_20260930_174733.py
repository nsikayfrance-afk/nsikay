from django.urls import path

from .operational_countries_views import (
    operational_countries,
    rollback_last_configuration,
)

from .operational_countries_history_views import (
    operational_countries_history,
)

from . import dashboard_views

from .country_statistics_views import (
    country_statistics,
)

from .administration_control_center_views import (
    administration_control_center,
)

from .global_administrative_log_views import (
    global_administrative_log,
)

from .service_country_control_views import (
    service_country_control,
)

from .activation_validation_views import (
    activation_validation,
)

from .certification_control_views import (
    certification_control,
)

from .financial_health_control_views import (
    financial_health_control,
)

from .final_activation_views import (
    final_activate_service,
)

from .final_deactivation_views import (
    final_deactivate_service,
)


app_name = "service_dashboard"


urlpatterns = [

    path(
        "operational-countries/",
        operational_countries,
        name="operational_countries",
    ),

    path(
        "operational-countries/history/",
        operational_countries_history,
        name="operational_countries_history",
    ),

    path(
        "operational-countries/history/rollback/",
        rollback_last_configuration,
        name="rollback_last_configuration",
    ),

    path(
        "",
        dashboard_views.dashboard_home,
        name="dashboard_home",
    ),

    path(
        "statistics/",
        dashboard_views.administration_statistics,
        name="administration_statistics",
    ),

    path(
        "statistics/countries/",
        country_statistics,
        name="country_statistics",
    ),

    path(
        "control-center/",
        administration_control_center,
        name="control_center",
    ),

    path(
        "control-center-filtered/",
        dashboard_views.control_center_filtered,
        name="control_center_filtered",
    ),

    path(
        "history/",
        dashboard_views.administration_history,
        name="administration_history",
    ),

    path(
        "administrative-log/",
        global_administrative_log,
        name="global_administrative_log",
    ),

    path(
        "service-country-control/",
        service_country_control,
        name="service_country_control",
    ),

    path(
        "activation-validation/",
        activation_validation,
        name="activation_validation",
    ),

    path(
        "certification-control/",
        certification_control,
        name="certification_control",
    ),

    path(
        "financial-health-control/",
        financial_health_control,
        name="financial_health_control",
    ),

    path(
        "final-activate/<int:activation_id>/",
        final_activate_service,
        name="final_activate_service",
    ),

    path(
        "final-deactivate/<int:activation_id>/",
        final_deactivate_service,
        name="final_deactivate_service",
    ),

    path(
        "activate/<int:activation_id>/",
        dashboard_views.activate_service,
        name="activate_service",
    ),

    path(
        "deactivate/<int:activation_id>/",
        dashboard_views.deactivate_service,
        name="deactivate_service",
    ),
]



