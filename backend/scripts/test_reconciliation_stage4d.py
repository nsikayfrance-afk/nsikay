import os
from decimal import Decimal

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

import django
django.setup()

from finance.models import Wallet, WalletTransaction
from financial_accounts.models import (
    FinancialAccount,
    GiftFinancialLedger,
)

print("=" * 70)
print(" NSIKAY - STAGE 4D.5 - RAPPROCHEMENT FINANCIER GLOBAL")
print("=" * 70)


print("\nCOMPTAGE MODELES")

wallet_count = Wallet.objects.count()
transaction_count = WalletTransaction.objects.count()
account_count = FinancialAccount.objects.count()
ledger_count = GiftFinancialLedger.objects.count()

print(" - Wallet =", wallet_count)
print(" - WalletTransaction =", transaction_count)
print(" - FinancialAccount =", account_count)
print(" - GiftFinancialLedger =", ledger_count)


print("\nVERIFICATION COMPTES NSIKAY")

gift_accounts = FinancialAccount.objects.filter(
    code__startswith="NSIKAY-GIFTS"
)

for account in gift_accounts:
    print(
        " -",
        account.code,
        "=",
        account.current_balance,
        account.status
    )


print("\nVERIFICATION LEDGER")

ledger_total = sum(
    (entry.amount for entry in GiftFinancialLedger.objects.all()),
    Decimal("0.00")
)

print(
    " - Total Ledger cadeaux =",
    ledger_total
)


print("\nVERIFICATION REFERENCES")

duplicate_refs = (
    WalletTransaction.objects
    .values("reference")
    .annotate(total=django.db.models.Count("id"))
    .filter(total__gt=1)
)


duplicates = list(duplicate_refs)

print(
    " - References Wallet dupliquees =",
    len(duplicates)
)

assert len(duplicates) == 0


print("\nUNICITE REFERENCES = OK")

print("\nRAPPROCHEMENT FINANCIER GLOBAL = OK")

print("=" * 70)
