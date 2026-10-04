from django.urls import path

from .views_secure import (

    WalletSecureBalanceView,
    WalletTransferView,
    WalletWithdrawView

)


urlpatterns = [

    path(
        "balance/",
        WalletSecureBalanceView.as_view()
    ),

    path(
        "transfer/",
        WalletTransferView.as_view()
    ),

    path(
        "withdraw/",
        WalletWithdrawView.as_view()
    ),

]

