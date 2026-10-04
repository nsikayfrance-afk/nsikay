from django.urls import path

from api_nsikay.marketplace_views import marketplace_products


app_name = "marketplace_legacy"


urlpatterns = [
    path(
        "products/",
        marketplace_products,
        name="products_legacy_disabled",
    ),
]
