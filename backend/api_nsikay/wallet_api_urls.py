from django.urls import path
from . import views

urlpatterns = [

    path(
        "balance/",
        views.wallet_balance,
        name="wallet-balance"
    ),

]

