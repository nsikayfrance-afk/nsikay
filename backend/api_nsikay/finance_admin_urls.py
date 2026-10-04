from django.urls import path

from api_nsikay.finance_admin_views import (
    finance_admin_dashboard
)


urlpatterns = [

    path(
        "",
        finance_admin_dashboard,
        name="finance-admin-dashboard"
    ),

]


