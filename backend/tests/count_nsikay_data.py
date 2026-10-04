from django.apps import apps

names = [
    "User",
    "Wallet",
    "WalletTransaction",
    "WenzeProduct",
    "WenzeOrder",
    "BukaPrixCampaign",
    "FinancialRoutingRule",
    "FinancialRoutingLog",
    "FinancialFeeRule",
    "FinancialPartner",
    "Transaction",
]

print("")
print("=" * 60)
print("COMPTAGE DONNEES NSIKAY")
print("=" * 60)

for name in names:
    model = None

    for candidate in apps.get_models():
        if candidate.__name__ == name:
            model = candidate
            break

    if model is not None:
        try:
            print(f"{name}: {model.objects.count()}")
        except Exception as exc:
            print(f"{name}: ERREUR - {exc}")
    else:
        print(f"{name}: MODELE NON TROUVE")

print("=" * 60)
