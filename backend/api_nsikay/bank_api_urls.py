from django.urls import path

from .bank_views import BanksListView


urlpatterns = [

    path(
        "",
        BanksListView.as_view()
    ),

]

