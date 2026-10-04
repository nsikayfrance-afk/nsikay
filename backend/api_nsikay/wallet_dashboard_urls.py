from django.urls import path

from api_nsikay.wallet_dashboard_views import (
    wallet_dashboard
)


urlpatterns = [

    path(
        "",
        wallet_dashboard,
        name="wallet-dashboard"
    ),

]


