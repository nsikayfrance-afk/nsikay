from django.urls import path
from . import views


urlpatterns = [

    path(
        "assign/<int:inspection_id>/<int:agent_id>/",
        views.assign_agent
    ),


    path(
        "submit/<int:inspection_id>/",
        views.submit_inspection
    ),


    path(
        "approve/<int:inspection_id>/",
        views.approve_certification
    ),

]

