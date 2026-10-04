from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

extra = '''

from banking.models import (
    Bank,
    BankAccount,
    BankingOperation,
    BankTransaction,
    BankBalance,
    AccountOpeningRequest
)


@login_required
def banque_stats(request):

    data = {

        "banques":
            Bank.objects.count(),

        "comptes":
            BankAccount.objects.count(),

        "operations":
            BankingOperation.objects.count(),

        "transactions":
            BankTransaction.objects.count(),

        "soldes":
            BankBalance.objects.count(),

        "demandes_ouverture":
            AccountOpeningRequest.objects.count(),

    }

    return JsonResponse({
        "dashboard": "Banque Partenaire NSIKAY",
        "user": request.user.username,
        "stats": data
    })

'''

if "def banque_stats" not in content:
    file.write_text(content + extra, encoding="utf-8")

print("=== DASHBOARD BANQUE AJOUTE ===")

