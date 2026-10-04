from django.urls import path
from . import views


urlpatterns = [

    path("stats/", views.dashboard_stats),

    path("banques/", views.banques_partenaires),

    path("pays/", views.supervision_pays),

    path("certification/", views.certification_stats),

    path("transactions/", views.transactions_stats),

    path("finance/", views.finance_stats),

]


from . import views

urlpatterns += [

    path(
        "control-center/",
        views.nsikay_control_center
    ),

]

