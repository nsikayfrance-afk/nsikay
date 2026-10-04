from pathlib import Path

print("=== CONNEXION DASHBOARD TRANSACTIONS REELLES NSIKAY ===")


path = Path("dashboard/views.py")

content = path.read_text(encoding="utf-8")


old = """
def transaction_stats(request):
    return JsonResponse({
        "module": "Transactions NSIKAY",
        "total_transactions": 0
    })
"""


new = """
def transaction_stats(request):

    from transactions.models import Transaction

    transactions = []

    total_amount = 0


    for tx in Transaction.objects.all().order_by("-id"):

        montant = getattr(tx, "amount", 0)

        try:
            total_amount += float(montant)
        except:
            pass


        transactions.append({

            "id": tx.id,

            "utilisateur":
                str(getattr(tx, "user", None)),

            "montant":
                montant,

            "devise":
                str(getattr(tx, "currency", "")),

            "statut":
                getattr(tx, "status", "UNKNOWN"),

            "type":
                getattr(tx, "transaction_type", "UNKNOWN"),

        })


    return JsonResponse({

        "module":
            "Transactions Réelles NSIKAY",

        "total_transactions":
            len(transactions),

        "volume_total":
            total_amount,

        "transactions":
            transactions

    })
"""


if old in content:

    content = content.replace(old,new)

else:

    print("Fonction transaction_stats existante différente")


path.write_text(content, encoding="utf-8")


print("=== DASHBOARD TRANSACTIONS MIS A JOUR ===")