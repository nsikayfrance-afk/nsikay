from django.urls import path

from .views import (
    PasswordRecoveryRequestView,
    PasswordRecoveryResetView,
    PasswordRecoveryVerifyView,
)


urlpatterns = [
    path(
        "request/",
        PasswordRecoveryRequestView.as_view(),
        name="password-recovery-request",
    ),
    path(
        "verify/",
        PasswordRecoveryVerifyView.as_view(),
        name="password-recovery-verify",
    ),
    path(
        "reset/",
        PasswordRecoveryResetView.as_view(),
        name="password-recovery-reset",
    ),
]
