from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

extra = '''

from django.db.models import Count, Sum
from finance.models import Wallet, Currency
from transactions.models import Transaction
from certification.models import CertificationCertificate
from administration.models import ValidationRequest


@login_required
def dashboard_stats(request):

    data = {

        "wallets":
            Wallet.objects.count(),

        "currencies":
            Currency.objects.count(),

        "transactions":
            Transaction.objects.count(),

        "certificates":
            CertificationCertificate.objects.count(),

        "validations":
            ValidationRequest.objects.count(),

    }

    return JsonResponse({
        "module": "NSIKAY Statistics",
        "data": data
    })

'''

if "dashboard_stats" not in content:
    file.write_text(content + extra, encoding="utf-8")

print("=== STATS DASHBOARD AJOUTEES ===")

