from django.urls import path

from . import views


urlpatterns = [

    # ========================================================
    # AUTHENTIFICATION
    # ========================================================

    path(
        "auth/register/",
        views.register,
        name="api-register"
    ),

    path(
        "auth/login/",
        views.login,
        name="api-login"
    ),

    path(
        "auth/logout/",
        views.logout,
        name="api-logout"
    ),

    path(
        "auth/me/",
        views.me,
        name="api-me"
    ),

    # ========================================================
    # PROFIL
    # ========================================================

    path(
        "profile/",
        views.profile,
        name="api-profile"
    ),

    path(
        "profile/update/",
        views.update_profile,
        name="api-profile-update"
    ),

    # ========================================================
    # MODULES
    # ========================================================

    path(
        "users/",
        views.users,
        name="api-users"
    ),

    path(
        "banks/",
        views.banks,
        name="api-banks"
    ),

    path(
        "countries/",
        views.countries,
        name="api-countries"
    ),

    path(
        "certifications/",
        views.certifications,
        name="api-certifications"
    ),

    path(
        "transactions/",
        views.transactions,
        name="api-transactions"
    ),

    path(
        "finance/",
        views.finance,
        name="api-finance"
    ),

]
