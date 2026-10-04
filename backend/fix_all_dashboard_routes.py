from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

compat = """

# === COMPATIBILITE ANCIENS ENDPOINTS DASHBOARD NSIKAY ===

@login_required
def certification_stats(request):
    return dashboard_certification(request)


@login_required
def transaction_stats(request):
    return dashboard_transactions(request)


@login_required
def finance_stats(request):
    return dashboard_finance(request)


@login_required
def pays_stats(request):
    return dashboard_pays(request)


@login_required
def banques_stats(request):
    return dashboard_banques(request)


@login_required
def dashboard_home(request):
    return dashboard_stats(request)

"""

if "def certification_stats" not in content:
    content += compat
    file.write_text(content, encoding="utf-8")

print("=== COMPATIBILITE DASHBOARD COMPLETE ===")


