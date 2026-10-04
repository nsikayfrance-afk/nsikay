from django.urls import path

from api_nsikay.enterprise_views import gateway_status



urlpatterns=[


path(

    "status/",

    gateway_status

),


]


