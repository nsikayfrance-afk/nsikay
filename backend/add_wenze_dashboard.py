from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

extra = '''

from finance.models import Wallet
from transactions.models import Transaction


@login_required
def wenze_stats(request):

    data = {

        "wallets":
            Wallet.objects.count(),

        "transactions":
            Transaction.objects.filter(
                transaction_type="TRANSFER"
            ).count(),

        "utilisateurs_wallet":
            Wallet.objects.values(
                "user"
            ).distinct().count(),

    }


    return JsonResponse({

        "dashboard":
            "Gestion WENZE NSIKAY",

        "user":
            request.user.username,

        "stats":
            data

    })

'''

if "def wenze_stats" not in content:
    file.write_text(content + extra, encoding="utf-8")

print("=== DASHBOARD WENZE AJOUTE ===")

