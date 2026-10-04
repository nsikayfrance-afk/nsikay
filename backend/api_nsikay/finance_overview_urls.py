from django.urls import path

from .finance_overview_views import finance_overview

urlpatterns = [
    path("", finance_overview, name="finance-overview"),
]
