import os
from decimal import Decimal

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

import django
django.setup()

from django.contrib.auth import get_user_model

from finance.models import Wallet, WalletTransaction
from financial_accounts.models import (
    FinancialAccount,
    GiftFinancialLedger,
)

print("=" * 70)
print(" NSIKAY - STAGE 4D.2 - TEST TRANSFERT FINANCIER")
print("=" * 70)


User = get_user_model()

sender = User.objects.filter(username="admin_test_nsikay").first()
receiver = User.objects.filter(username="validation_test_nsikay").first()


if not sender or not receiver:
    raise Exception(
        "Utilisateurs de test absents."
    )


sender_wallet = Wallet.objects.filter(
    user=sender
).first()

receiver_wallet = Wallet.objects.filter(
    user=receiver
).first()


if not sender_wallet or not receiver_wallet:
    raise Exception(
        "Wallets absents."
    )


print("\nUTILISATEURS")
print(" - Expéditeur :", sender.username)
print(" - Bénéficiaire :", receiver.username)


amount = Decimal("10.00")
commission = Decimal("0.50") / Decimal("100")
fee = amount * commission
received = amount - fee


print("\nCALCUL")
print(" - Montant transfert =", amount)
print(" - Commission NSIKAY =", fee)
print(" - Montant reçu =", received)


assert fee == Decimal("0.05")
assert received == Decimal("9.95")


print("\nCONTROLE REGLE 0.50% = OK")


print("\nMODELES DISPONIBLES")
print(" - WalletTransaction =", WalletTransaction.objects.count())
print(" - Ledger =", GiftFinancialLedger.objects.count())


print("\nSTAGE 4D.2 PREPARATION TRANSFERT = OK")

print("=" * 70)
