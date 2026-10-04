from django.urls import path

from api_nsikay.wallet_operations_views import (
    wallet_deposit,
    wallet_withdraw,
    wallet_transfer
)


urlpatterns = [

    path(
        "deposit/",
        wallet_deposit,
        name="wallet-deposit"
    ),

    path(
        "withdraw/",
        wallet_withdraw,
        name="wallet-withdraw"
    ),

    path(
        "transfer/",
        wallet_transfer,
        name="wallet-transfer"
    ),

]


