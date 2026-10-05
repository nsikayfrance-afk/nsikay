from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from nsikay.frontend_views import frontend_index, frontend_static

from nsikay_activities.views import (
    ActivityDashboardView,
    ActivityListCreateView,
    ActivityDetailView,
    ServiceListCreateView,
    ServiceDetailView,
    ProjectListCreateView,
    ProjectDetailView,
)

urlpatterns = [
    path("api/jobs/", include("jobs.urls")),
    path("assets/<path:path>", frontend_static, {"folder": "assets"}),
    path("images/<path:path>", frontend_static, {"folder": "images"}),
    path("favicon.svg", frontend_static, {"path": "favicon.svg", "folder": ""}, name="frontend-favicon"),
    path("icons.svg", frontend_static, {"path": "icons.svg", "folder": ""}, name="frontend-icons"),
    path("", frontend_index, name="frontend-home"),
    path("transport/", include("transport.urls")),
    path("api/media-library/", include("media_library.urls")),
    path("api/events/", include("events.urls")),
    path("api/tv/", include("api_nsikay.tv.urls")),

    # ========================================================
    # API ACTIVITES NSIKAY
    # ========================================================

    path(
        "api/activities/",
        include("nsikay_activities.urls"),
    ),

    # ========================================================
    # COMPATIBILITE ACTIVITES
    # ========================================================

    path(
        "api/dashboard/",
        ActivityDashboardView.as_view(),
        name="activities-dashboard-compat",
    ),

    path(
        "api/projects/",
        ProjectListCreateView.as_view(),
        name="projects-list-create-compat",
    ),

    path(
        "api/projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail-compat",
    ),

    # ========================================================
    # SERVICES SYSTEME
    #
    # IMPORTANT :
    # /api/services/ appartient Ã¢â€Å“ÃƒÂ¢ÃƒÂ£Ãƒâ€ Ã¢â€Å“ÃƒÂ©Ã¢â€Â¬ÃƒÂ¡ service_control.
    # Les services liÃ¢â€Å“ÃƒÂ¢ÃƒÂ£Ãƒâ€ Ã¢â€Å“ÃƒÂ©Ã¢â€Â¬Ã‚Â®s Ã¢â€Å“ÃƒÂ¢ÃƒÂ£Ãƒâ€ Ã¢â€Å“ÃƒÂ©Ã¢â€Â¬ÃƒÂ¡ une activitÃ¢â€Å“ÃƒÂ¢ÃƒÂ£Ãƒâ€ Ã¢â€Å“ÃƒÂ©Ã¢â€Â¬Ã‚Â® sont sous :
    # /api/activities/services/
    # ========================================================

    path(
        "api/services/",
        include("service_control.urls"),
    ),

    # ========================================================
    # API GENERALE NSIKAY
    # ========================================================

    path(
        "api/",
        include("api.urls"),
    ),

    # ========================================================
    # ADMINISTRATION
    # ========================================================

    path(
        "admin/",
        admin.site.urls,
    ),

    # ========================================================
    # MODULES DJANGO EXISTANTS
    # ========================================================

    path(
        "banking/",
        include("banking.urls"),
    ),

    path(
        "dashboard/",
        include("dashboard.urls"),
    ),

    path(
        "certification/",
        include("certification.urls"),
    ),

    path(
        "administration/",
        include("administration.urls"),
    ),

    path(
        "transactions/",
        include("transactions.urls"),
    ),

    path(
        "partners/",
        include("partner_finance.urls"),
    ),

    path(
        "finance/",
        include("finance.urls"),
    ),

    path(
        "business/",
        include("business.urls"),
    ),

    path(
        "wenze/",
        include("wenze.urls"),
    ),

    path(
        "marketing/",
        include("marketing.urls"),
    ),

    path(
        "media/",
        include("media.urls"),
    ),

    path(
        "ai/",
        include("ai.urls"),
    ),

    path(
        "operations/",
        include("operations.urls"),
    ),

    path(
        "association/",
        include("association.urls"),
    ),

    path(
        "app-center/",
        include("app_center.urls"),
    ),

    path(
        "bank-dashboard/",
        include("bank_dashboard.urls"),
    ),

    path(
        "service-dashboard/",
        include("service_dashboard.urls"),
    ),

    path(
        "dashboard/tv-regie/",
        include("tv_regie.dashboard_urls"),
    ),

    # ========================================================
    # API NSIKAY SPECIALISEE
    # ========================================================

    path(
        "api/nsikay/",
        include("api_nsikay.urls"),
    ),

    path(
        "api/tv-regie/",
        include("tv_regie.urls"),
    ),

    # ========================================================
    # FRONTEND REACT / SPA FALLBACK
    # ========================================================

    path(
        "<path:path>",
        frontend_index,
        name="frontend-spa-fallback",
    ),
]


# ============================================================
# MEDIA - DEVELOPPEMENT
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

