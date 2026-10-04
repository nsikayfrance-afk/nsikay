from django.urls import path

from . import views


urlpatterns = [

    # --------------------------------------------------------
    # ROUTES HISTORIQUES - COMPATIBILITE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # ROUTES CANONIQUES NSIKAY MEMBERSHIP
    # --------------------------------------------------------

    path(
        "membership/",
        views.membership_me,
        name="membership-me-canonical",
    ),

    path(
        "membership/types/",
        views.membership_types,
        name="membership-types-canonical",
    ),

    path(
        "membership/apply/",
        views.membership_apply,
        name="membership-apply-canonical",
    ),

    path(
        "membership/card/",
        views.membership_card,
        name="membership-card-canonical",
    ),

    path(
        "membership/verify/<str:token>/",
        views.membership_verify,
        name="membership-verify-canonical",
    ),

    path(
        "membership/applications/",
        views.membership_applications,
        name="membership-applications-canonical",
    ),

    path(
        "membership/applications/<int:application_id>/review/",
        views.membership_review,
        name="membership-review-canonical",
    ),
]
