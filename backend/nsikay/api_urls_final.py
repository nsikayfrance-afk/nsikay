from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)


from django.urls import path, include


urlpatterns = [

    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain"
    ),

    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),


    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),


    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui"
    ),


    path(
        "wallet/",
        include("wallet.urls")
    ),

    path(
        "nsikay/",
        include("api_nsikay.urls")
    ),

]

