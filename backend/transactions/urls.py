from django.urls import path

from . import views


urlpatterns = [

    path(

        "execute/<int:transaction_id>/",

        views.execute_transaction

    ),

]

