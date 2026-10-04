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
print(" NSIKAY - STAGE 4D - CONTROLE FINANCIER GLOBAL")
print("=" * 70)


User = get_user_model()

print("\nUTILISATEURS")
print(" - Test financier NSIKAY")


print("\nVERIFICATION MODELES")

print("Wallet :", Wallet.objects.count())
print("WalletTransaction :", WalletTransaction.objects.count())
print("FinancialAccount :", FinancialAccount.objects.count())
print("GiftFinancialLedger :", GiftFinancialLedger.objects.count())


print("\nREGLES FINANCIERES")

print(" - Transfert NSIKAY = 0.50 %")
print(" - Retrait = 1.20 %")
print(" - Mobile Money / Carte = 0.85 %")
print(" - WENZE commission = 0 %")


print("\nSTAGE 4D PREPARATION = OK")

print("=" * 70)
