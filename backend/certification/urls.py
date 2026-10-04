from django.urls import path
from . import views
from .activity_api import (
    ActivityCertificationListView,
    ActivityCertificationDetailView,
    ActivityCertificationHistoryView,
    ActivityCertificationActionView,
)


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

    # --------------------------------------------------------
    # API CERTIFICATION DES ACTIVITES
    # --------------------------------------------------------

    path(
        "activity-certifications/",
        ActivityCertificationListView.as_view(),
        name="activity-certifications-list",
    ),

    path(
        "activity-certifications/<int:certification_id>/",
        ActivityCertificationDetailView.as_view(),
        name="activity-certification-detail",
    ),

    path(
        "activity-certifications/<int:certification_id>/history/",
        ActivityCertificationHistoryView.as_view(),
        name="activity-certification-history",
    ),

    path(
        "activity-certifications/<int:certification_id>/<str:action>/",
        ActivityCertificationActionView.as_view(),
        name="activity-certification-action",
    ),

]

