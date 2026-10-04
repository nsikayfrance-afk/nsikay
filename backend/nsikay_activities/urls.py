from django.urls import path

from .views import (
    ActivityDashboardView,
    ActivityListCreateView,
    ActivityDetailView,
    ServiceListCreateView,
    ServiceDetailView,
    ProjectListCreateView,
    ProjectDetailView,
)

urlpatterns = [
    path(
        "dashboard/",
        ActivityDashboardView.as_view(),
        name="activities-dashboard",
    ),

    path(
        "",
        ActivityListCreateView.as_view(),
        name="activities-list-create",
    ),

    path(
        "<int:pk>/",
        ActivityDetailView.as_view(),
        name="activity-detail",
    ),

    path(
        "services/",
        ServiceListCreateView.as_view(),
        name="services-list-create",
    ),

    path(
        "services/<int:pk>/",
        ServiceDetailView.as_view(),
        name="service-detail",
    ),

    path(
        "projects/",
        ProjectListCreateView.as_view(),
        name="projects-list-create",
    ),

    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
]
