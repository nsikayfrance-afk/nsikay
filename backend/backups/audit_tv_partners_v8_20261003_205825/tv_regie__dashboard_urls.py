from django.urls import path

from .dashboard_views import tv_regie_dashboard


urlpatterns = [
    path(
        "",
        tv_regie_dashboard,
        name="tv_regie_dashboard"
    ),
]

