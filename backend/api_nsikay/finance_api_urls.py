from django.urls import path

from .finance_views import FinanceStatusView


urlpatterns = [

    path(
        "status/",
        FinanceStatusView.as_view()
    )

]

