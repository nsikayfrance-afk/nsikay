from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import transaction

from finance.models import Currency, Wallet
from financial_accounts.models import FinancialAccount

from gift_resellers.financial_service import (
    money,
    get_user_wallet,
    validate_sale_financial_destination,
)

print("=" * 70)
print(" NSIKAY - STAGE 4A - VALIDATION MOTEUR FINANCIER")
print("=" * 70)

print("\nDEVISES :")

for code in ["CDF", "EUR", "USD"]:
    obj = Currency.objects.filter(code=code).first()
    print(
        f" - {code} : "
        + ("OK" if obj else "ABSENTE")
    )

print("\nCOMPTES CADEAUX :")

for code in [
    "NSIKAY-GIFTS-CDF",
    "NSIKAY-GIFTS-EUR",
    "NSIKAY-GIFTS-USD",
]:
    account = FinancialAccount.objects.filter(code=code).first()

    if account:
        print(
            f" - {code} | "
            f"status={account.status} | "
            f"currency={account.currency} | "
            f"balance={account.current_balance}"
        )
    else:
        print(f" - {code} | ABSENT")

print("\nPORTEFEUILLES :")

User = get_user_model()

for username in [
    "banque_test_nsikay",
    "validation_test_nsikay",
    "admin_test_nsikay",
]:
    user = User.objects.filter(username=username).first()

    if not user:
        print(f" - {username} : UTILISATEUR ABSENT")
        continue

    wallets = Wallet.objects.filter(user=user)

    if not wallets.exists():
        print(f" - {username} : AUCUN PORTEFEUILLE")
        continue

    for wallet in wallets:
        print(
            f" - {username} | "
            f"id={wallet.id} | "
            f"currency={wallet.currency.code} | "
            f"balance={wallet.balance} | "
            f"active={wallet.active}"
        )

print("\nTEST DE PROTECTION DES COMPTES :")

for code in [
    "NSIKAY-GIFTS-CDF",
    "NSIKAY-GIFTS-EUR",
    "NSIKAY-GIFTS-USD",
]:
    account = FinancialAccount.objects.filter(code=code).first()

    if account and account.status != FinancialAccount.AccountStatus.ACTIVE:
        print(
            f" - {code} : PROTECTION OK "
            f"(règlement réel refusé tant que status={account.status})"
        )

print("\nTEST PORTEFEUILLE EUR :")

admin = User.objects.filter(username="admin_test_nsikay").first()

if admin:
    try:
        get_user_wallet(admin, "EUR")
        print(" - EUR : PORTEFEUILLE DISPONIBLE")
    except Exception as exc:
        print(f" - EUR : ATTENDU / NON DISPONIBLE -> {exc}")

print("\nTEST GARDE REPARTITION :")

class FakeAllocation:
    def __init__(self, amount, allocation_type):
        self.amount = Decimal(amount)
        self.allocation_type = allocation_type

class FakeAllocations:
    def __init__(self, items):
        self._items = items

    def all(self):
        return self._items

    def filter(self, **kwargs):
        key = kwargs.get("allocation_type")
        return [
            x for x in self._items
            if x.allocation_type == key
        ]

class FakeSale:
    retail_amount = Decimal("600.00")

    def __init__(self):
        self.allocations = FakeAllocations([
            FakeAllocation("360.00", "MEMBER"),
            FakeAllocation("180.00", "PRINCIPAL_RESELLER"),
            FakeAllocation("0.01", "NSIKAY"),
            FakeAllocation("30.00", "OTHER"),
        ])

try:
    validate_sale_financial_destination(FakeSale())
    print(" - ERREUR : la répartition aurait dû être refusée")
except Exception as exc:
    print(f" - PROTECTION OK : {exc}")

print("\n" + "=" * 70)
print(" STAGE 4A : MOTEUR FINANCIER PREPARE")
print("=" * 70)
print("Aucun solde réel existant n'a été modifié par ce test.")