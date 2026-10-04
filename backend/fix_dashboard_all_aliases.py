from pathlib import Path

views = Path("dashboard/views.py")

content = views.read_text(encoding="utf-8")

aliases = """

# === ALIASES COMPATIBILITE DASHBOARD NSIKAY ===

try:
    dashboard_stats
except NameError:
    def dashboard_stats(request):
        return stats_dashboard(request)


try:
    banques_partenaires
except NameError:
    def banques_partenaires(request):
        return bank_dashboard(request)


try:
    certification_stats
except NameError:
    def certification_stats(request):
        return certification_dashboard(request)


try:
    transactions_stats
except NameError:
    def transactions_stats(request):
        return transaction_stats(request)


try:
    finance_stats
except NameError:
    def finance_stats(request):
        return finance_dashboard(request)


print("=== ALIASES DASHBOARD NSIKAY FINALISES ===")

"""

if "ALIASES COMPATIBILITE DASHBOARD NSIKAY" not in content:
    with views.open("a", encoding="utf-8") as f:
        f.write(aliases)

print("=== ALIASES DASHBOARD AJOUTES ===")