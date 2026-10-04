from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

extra = '''

from django.db.models import Sum
from finance.models import Wallet, Currency, ExchangeRate
from transactions.models import Transaction


@login_required
def finance_stats(request):

    total_transactions = Transaction.objects.count()

    total_volume = (
        Transaction.objects.aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )


    data = {

        "transactions":
            total_transactions,

        "volume_total":
            str(total_volume),

        "wallets":
            Wallet.objects.count(),

        "devises":
            Currency.objects.count(),

        "taux_change":
            ExchangeRate.objects.count(),

    }


    return JsonResponse({

        "dashboard":
            "Contrôle Financier NSIKAY",

        "user":
            request.user.username,

        "stats":
            data

    })

'''

if "def finance_stats" not in content:
    file.write_text(content + extra, encoding="utf-8")

print("=== DASHBOARD FINANCE AJOUTE ===")

