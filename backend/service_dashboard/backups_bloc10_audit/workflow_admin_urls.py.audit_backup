from django.urls import path

from .workflow_admin_views import (
    workflow_dashboard,
    workflow_create_request,
    workflow_detail,
    workflow_validate,
    workflow_reject,
    workflow_activate,
)


urlpatterns = [
    path(
        "",
        workflow_dashboard,
        name="workflow_admin_dashboard",
    ),

    path(
        "create/",
        workflow_create_request,
        name="workflow_admin_create",
    ),

    path(
        "<int:request_id>/",
        workflow_detail,
        name="workflow_admin_detail",
    ),

    path(
        "<int:request_id>/validate/",
        workflow_validate,
        name="workflow_admin_validate",
    ),

    path(
        "<int:request_id>/reject/",
        workflow_reject,
        name="workflow_admin_reject",
    ),

    path(
        "<int:request_id>/activate/",
        workflow_activate,
        name="workflow_admin_activate",
    ),
]