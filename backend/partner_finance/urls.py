from django.urls import path

from . import views


urlpatterns = [

    path(
        "dashboard/",
        views.partner_dashboard
    ),

    path(
        "certification/",
        views.request_certification
    ),

    path(
        "supply/",
        views.request_supply
    ),

]

