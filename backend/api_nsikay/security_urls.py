from django.urls import path

from rest_framework_simplejwt.views import (

    TokenObtainPairView,

    TokenRefreshView

)


from api_nsikay.security_views import security_profile



urlpatterns=[


path(

    "token/",

    TokenObtainPairView.as_view()

),


path(

    "refresh/",

    TokenRefreshView.as_view()

),


path(

    "profile/",

    security_profile

),


]


