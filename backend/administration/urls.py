from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.admin_dashboard,
        name="admin_dashboard"
    ),


    path(
        "bank/approve/<int:id>/",
        views.approve_bank
    ),


    path(
        "currency/approve/<int:id>/",
        views.approve_currency
    ),


    path(
        "partner/approve/<int:id>/",
        views.approve_partner
    ),

]

