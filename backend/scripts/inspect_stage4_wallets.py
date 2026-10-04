import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.contrib.auth import get_user_model
from finance.models import Wallet, Currency

User = get_user_model()

print("=" * 70)
print("DEVISES DISPONIBLES")
print("=" * 70)

for currency in Currency.objects.all().order_by("code"):
    print(
        f"ID={currency.id} | "
        f"CODE={currency.code} | "
        f"NOM={getattr(currency, 'name', '')}"
    )

print("")
print("=" * 70)
print("PORTEFEUILLES DES UTILISATEURS STAGE 4")
print("=" * 70)

usernames = [
    "banque_test_nsikay",
    "validation_test_nsikay",
    "admin_test_nsikay",
]

for username in usernames:
    print("")
    print(f"UTILISATEUR : {username}")

    user = User.objects.filter(username=username).first()

    if not user:
        print("  UTILISATEUR INTROUVABLE")
        continue

    wallets = Wallet.objects.filter(user=user).select_related("currency")

    if not wallets.exists():
        print("  AUCUN PORTEFEUILLE")
        continue

    for wallet in wallets:
        print(
            f"  WALLET ID={wallet.id} | "
            f"currency={wallet.currency.code} | "
            f"balance={wallet.balance} | "
            f"active={wallet.active}"
        )

print("")
print("=" * 70)
print("COMPTES CADEAUX FINANCIERS")
print("=" * 70)

from financial_accounts.models import FinancialAccount

for code in [
    "NSIKAY-GIFTS-EUR",
    "NSIKAY-GIFTS-USD",
    "NSIKAY-GIFTS-CDF",
]:
    account = FinancialAccount.objects.filter(code=code).first()

    if account:
        print(
            f"{account.code} | "
            f"status={account.status} | "
            f"currency={account.currency} | "
            f"balance={account.current_balance}"
        )
    else:
        print(f"{code} | INTROUVABLE")

print("")
print("=" * 70)
print("INSPECTION PORTEFEUILLES = TERMINEE")
print("=" * 70)