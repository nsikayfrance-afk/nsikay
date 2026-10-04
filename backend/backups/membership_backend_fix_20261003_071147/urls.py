from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.membership_me,
        name="membership-me",
    ),

    path(
        "types/",
        views.membership_types,
        name="membership-types",
    ),

    path(
        "apply/",
        views.membership_apply,
        name="membership-apply",
    ),

    path(
        "card/",
        views.membership_card,
        name="membership-card",
    ),

    path(
        "verify/<str:token>/",
        views.membership_verify,
        name="membership-verify",
    ),

    path(
        "applications/",
        views.membership_applications,
        name="membership-applications",
    ),

    path(
        "applications/<int:application_id>/review/",
        views.membership_review,
        name="membership-review",
    ),
]
