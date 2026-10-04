from django.urls import path

from api_nsikay.wallet_bank_views import (

    add_bank_account,

    wallet_banks

)


urlpatterns=[


path(

    "add/",

    add_bank_account

),


path(

    "<int:wallet_id>/",

    wallet_banks

),


]


