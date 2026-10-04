from pathlib import Path

file = Path("dashboard/views.py")

content = '''

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def dashboard_response(request, role):

    return JsonResponse({
        "module": "NSIKAY Dashboard",
        "role": role,
        "user": request.user.username,
        "status": "active"
    })


@login_required
def admin_dashboard(request):
    return dashboard_response(request, "Super Administrateur NSIKAY")


@login_required
def pays_dashboard(request):
    return dashboard_response(request, "Administration Pays")


@login_required
def banque_dashboard(request):
    return dashboard_response(request, "Banque Partenaire")


@login_required
def finance_dashboard(request):
    return dashboard_response(request, "Contrôleur Financier")


@login_required
def wenze_dashboard(request):
    return dashboard_response(request, "Gestionnaire WENZE")


@login_required
def certification_dashboard(request):
    return dashboard_response(request, "Autorité de Certification")


@login_required
def conformite_dashboard(request):
    return dashboard_response(request, "Superviseur Conformité")


@login_required
def publicite_dashboard(request):
    return dashboard_response(request, "Gestionnaire Publicité")


@login_required
def evenements_dashboard(request):
    return dashboard_response(request, "Gestionnaire Événements")
'''

with open(file, "a", encoding="utf-8") as f:
    f.write(content)

print("=== DASHBOARD VIEWS NSIKAY CREES ===")

