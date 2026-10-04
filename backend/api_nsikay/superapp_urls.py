from django.urls import path

from api_nsikay.superapp_views import social_feed



urlpatterns=[

    path(

        "feed/",

        social_feed

    ),

]


