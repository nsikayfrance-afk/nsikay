from django.urls import path, include


urlpatterns = [

    path(
        "banks/",
        include("api_nsikay.banks_urls")
    ),

    path(
        "countries/",
        include("api_nsikay.countries_urls")
    ),

    path(
        "transactions/",
        include("api_nsikay.transactions_urls")
    ),

    path(
        "finance/",
        include("api_nsikay.finance_urls")
    ),

    path(
        "wallet/",
        include("api_nsikay.wallet_api_urls")
    ),

]

path(
    "wallet/operations/",
    include("api_nsikay.wallet_operations_urls")
),


path(
    "wallet/dashboard/",
    include("api_nsikay.wallet_dashboard_urls")
),


path(
    "wallet/banks/",
    include("api_nsikay.wallet_bank_urls")
),


path(
    "admin/finance/",
    include("api_nsikay.finance_admin_urls")
),


path(
    "security/",
    include("api_nsikay.security_urls")
),
,


path(
    "superapp/",
    include("api_nsikay.superapp_urls")
),


path(
    "analytics/",
    include("api_nsikay.analytics_urls")
),


path(
    "enterprise/",
    include("api_nsikay.enterprise_urls")
),



path("tv/", include("api_nsikay.tv.urls")),






