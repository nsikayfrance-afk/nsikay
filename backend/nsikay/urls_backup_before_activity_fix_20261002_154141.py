from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, path, include


urlpatterns = [
    path('api/', include('nsikay_activities.urls')),
    path("api/services/", include("service_control.urls")),
    path('api/', include('api.urls')),

    path("admin/", admin.site.urls),

    path("banking/", include("banking.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("certification/", include("certification.urls")),
    path("administration/", include("administration.urls")),
    path("transactions/", include("transactions.urls")),
    path("partners/", include("partner_finance.urls")),

    path("finance/", include("finance.urls")),
    path("business/", include("business.urls")),
    path("wenze/", include("wenze.urls")),
    path("marketing/", include("marketing.urls")),
    path("media/", include("media.urls")),
    path("ai/", include("ai.urls")),
    path("operations/", include("operations.urls")),
    path("association/", include("association.urls")),
    path("app-center/", include("app_center.urls")),
    path("bank-dashboard/", include("bank_dashboard.urls")),
    path("service-dashboard/", include("service_dashboard.urls")),
    path("dashboard/tv-regie/", include("tv_regie.dashboard_urls")),

    path("api/nsikay/", include("api_nsikay.urls")),
    path("api/tv-regie/", include("tv_regie.urls")),
]














# NSIKAY - fichiers media en environnement de developpement
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

