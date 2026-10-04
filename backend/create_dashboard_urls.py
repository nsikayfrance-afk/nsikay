from pathlib import Path

file = Path("dashboard/urls.py")

content = '''
from django.urls import path
from . import views


urlpatterns = [

    path("admin/", views.admin_dashboard),
    path("pays/", views.pays_dashboard),
    path("banque/", views.banque_dashboard),
    path("finance/", views.finance_dashboard),
    path("wenze/", views.wenze_dashboard),
    path("certification/", views.certification_dashboard),
    path("conformite/", views.conformite_dashboard),
    path("publicite/", views.publicite_dashboard),
    path("evenements/", views.evenements_dashboard),

]
'''

file.write_text(content, encoding="utf-8")

print("=== DASHBOARD URLS NSIKAY CREES ===")

