from django.urls import path
from . import views


urlpatterns = [

    path(
        "dashboard/",
        views.bank_dashboard
    ),


    path(
        "account/accept/<int:account_id>/",
        views.accept_account
    ),


    path(
        "account/activate/<int:account_id>/",
        views.activate_account
    ),


    path(
        "account/reject/<int:account_id>/",
        views.reject_account
    ),

]

