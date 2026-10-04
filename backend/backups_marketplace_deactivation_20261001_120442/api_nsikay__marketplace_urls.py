from django.urls import path

from api_nsikay.marketplace_views import (

    marketplace_products

)



urlpatterns=[


path(

    "products/",

    marketplace_products

),


]


