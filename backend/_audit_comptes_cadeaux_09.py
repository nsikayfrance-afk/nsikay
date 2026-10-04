import os
from pathlib import Path
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.apps import apps
from django.contrib.auth.models import User

lines = []

def section(title):
    lines.append("")
    lines.append("=" * 70)
    lines.append(title)
    lines.append("=" * 70)

section("NSIKAY - AUDIT COMPTES CADEAUX 09")
lines.append("LECTURE SEULE - AUCUNE MODIFICATION")

# ------------------------------------------------------------
# FINANCIAL ACCOUNTS
# ------------------------------------------------------------
section("FINANCIAL ACCOUNTS")

FinancialAccount = apps.get_model(
    "financial_accounts",
    "FinancialAccount"
)

for account in FinancialAccount.objects.all().order_by(
    "account_type",
    "currency",
    "code"
):
    lines.append(
        f"ID={account.id} | "
        f"CODE={account.code} | "
        f"NOM={account.name} | "
        f"TYPE={account.account_type} | "
        f"DEVISE={account.currency} | "
        f"STATUT={account.status} | "
        f"SOLDE={account.current_balance} | "
        f"PARTENAIRE={account.bank_partner} | "
        f"INTERNE={account.is_internal_ledger}"
    )

lines.append("")
lines.append(
    f"TOTAL COMPTES : {FinancialAccount.objects.count()}"
)

for currency in ["EUR", "USD", "CDF"]:
    qs = FinancialAccount.objects.filter(
        account_type="GIFTS",
        currency=currency
    )

    lines.append(
        f"GIFTS {currency} : {qs.count()}"
    )

# ------------------------------------------------------------
# GIFT LEDGER
# ------------------------------------------------------------
section("GIFT FINANCIAL LEDGER")

GiftFinancialLedger = apps.get_model(
    "financial_accounts",
    "GiftFinancialLedger"
)

lines.append(
    f"TOTAL ECRITURES CADEAUX : "
    f"{GiftFinancialLedger.objects.count()}"
)

for row in GiftFinancialLedger.objects.all().order_by("-id")[:20]:
    lines.append(
        f"ID={row.id} | "
        f"REF={row.reference} | "
        f"TYPE={row.operation_type} | "
        f"DEV={row.currency} | "
        f"MONTANT={row.amount} | "
        f"ACHETEUR={row.buyer_reference} | "
        f"EMETTEUR={row.sender_reference} | "
        f"BENEFICIAIRE={row.beneficiary_reference} | "
        f"COMPTE={row.financial_account_id} | "
        f"RELATED={row.related_reference}"
    )

# ------------------------------------------------------------
# FINANCE WALLET
# ------------------------------------------------------------
section("FINANCE WALLET")

Wallet = apps.get_model("finance", "Wallet")
Currency = apps.get_model("finance", "Currency")
WalletTransaction = apps.get_model(
    "finance",
    "WalletTransaction"
)

lines.append(f"WALLETS : {Wallet.objects.count()}")
lines.append(
    f"CURRENCIES : {Currency.objects.count()}"
)
lines.append(
    f"WALLET TRANSACTIONS : "
    f"{WalletTransaction.objects.count()}"
)

for wallet in Wallet.objects.select_related(
    "user",
    "currency"
).order_by("id")[:50]:

    lines.append(
        f"WALLET ID={wallet.id} | "
        f"USER={wallet.user.username} | "
        f"CURRENCY={wallet.currency.code if hasattr(wallet.currency, 'code') else wallet.currency_id} | "
        f"BALANCE={wallet.balance} | "
        f"ACTIVE={wallet.active}"
    )

# ------------------------------------------------------------
# VIRTUAL GIFTS
# ------------------------------------------------------------
section("VIRTUAL GIFTS")

VirtualGift = apps.get_model(
    "api_nsikay",
    "VirtualGift"
)

GiftTransaction = apps.get_model(
    "api_nsikay",
    "GiftTransaction"
)

lines.append(
    f"CATALOGUE CADEAUX : {VirtualGift.objects.count()}"
)

for gift in VirtualGift.objects.all().order_by("value"):
    lines.append(
        f"GIFT ID={gift.id} | "
        f"NOM={gift.name} | "
        f"VALEUR={gift.value} | "
        f"DEVISE={gift.currency}"
    )

lines.append(
    f"TRANSACTIONS CADEAUX : "
    f"{GiftTransaction.objects.count()}"
)

# ------------------------------------------------------------
# CURRENCIES
# ------------------------------------------------------------
section("DEVISES")

for currency in Currency.objects.all().order_by("id"):
    lines.append(
        f"ID={currency.id} | "
        f"OBJET={currency}"
    )

# ------------------------------------------------------------
# FIN
# ------------------------------------------------------------
section("FIN")

OUT = Path(
    r"C:\Users\DELL Technologies\Desktop\nsikay nante"
    r"\reports\gifts\AUDIT_COMPTES_CADEAUX_09.txt"
)

OUT.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print("=" * 70)
print("AUDIT COMPTES CADEAUX 09 TERMINE")
print("=" * 70)
print("AUCUNE MODIFICATION EFFECTUEE")
print(f"Rapport : {OUT}")