from django.urls import path

from .views import (
    ActivityListCreateView,
    ActivityDetailView,
    ServiceListCreateView,
    ServiceDetailView,
    ProjectListCreateView,
    ProjectDetailView,
)

urlpatterns = [
    path(
        "activities/",
        ActivityListCreateView.as_view(),
        name="activities-list-create",
    ),
    path(
        "activities/<int:pk>/",
        ActivityDetailView.as_view(),
        name="activities-detail",
    ),
    path(
        "services/",
        ServiceListCreateView.as_view(),
        name="services-list-create",
    ),
    path(
        "services/<int:pk>/",
        ServiceDetailView.as_view(),
        name="services-detail",
    ),
    path(
        "projects/",
        ProjectListCreateView.as_view(),
        name="projects-list-create",
    ),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="projects-detail",
    ),
]
