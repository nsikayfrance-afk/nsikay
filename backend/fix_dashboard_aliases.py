from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

aliases = """

# === ALIASES COMPATIBILITE URLS NSIKAY ===

@login_required
def banques_partenaires(request):
    return dashboard_banques(request)


@login_required
def supervision_pays(request):
    return dashboard_pays(request)


@login_required
def certification_dashboard(request):
    return dashboard_certification(request)


@login_required
def transactions_dashboard(request):
    return dashboard_transactions(request)


@login_required
def finance_dashboard(request):
    return dashboard_finance(request)

"""

if "def banques_partenaires" not in content:
    content += aliases
    file.write_text(content, encoding="utf-8")


print("=== ALIASES DASHBOARD NSIKAY AJOUTES ===")


