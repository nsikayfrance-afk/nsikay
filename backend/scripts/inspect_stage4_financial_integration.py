import os
import inspect
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.apps import apps

print("=" * 70)
print("MODELES FINANCIERS ACTIFS")
print("=" * 70)

targets = [
    ("finance", "Wallet"),
    ("finance", "WalletTransaction"),
    ("finance", "FinancialLedger"),
    ("wallet", "Wallet"),
    ("wallet", "WalletBalance"),
    ("wallet", "WalletTransaction"),
    ("wallet", "WalletOperation"),
    ("financial_accounts", "FinancialAccount"),
    ("financial_accounts", "GiftFinancialLedger"),
    ("gift_resellers", "ResellerSale"),
    ("gift_resellers", "SaleAllocation"),
]

for app_label, model_name in targets:
    try:
        Model = apps.get_model(app_label, model_name)
        print(f"\n--- {app_label}.{model_name} ---")
        print("TABLE:", Model._meta.db_table)
        for field in Model._meta.fields:
            print(
                f"  {field.name} | "
                f"type={field.__class__.__name__} | "
                f"null={field.null} | "
                f"default={field.default!r}"
            )
    except Exception as exc:
        print(f"\n--- {app_label}.{model_name} ---")
        print("ERREUR:", repr(exc))

print("")
print("=" * 70)
print("SERVICES WALLET FINANCE")
print("=" * 70)

try:
    import finance.wallet_service as ws

    print("MODULE :", ws.__file__)

    for name in [
        "credit_wallet",
        "debit_wallet",
        "transfer_wallet",
    ]:
        fn = getattr(ws, name, None)

        if fn is None:
            print(f"\n{name} : INTROUVABLE")
        else:
            print(f"\n{name} :")
            print(inspect.signature(fn))
            try:
                print(inspect.getsource(fn))
            except Exception as exc:
                print("SOURCE NON DISPONIBLE :", repr(exc))

except Exception as exc:
    print("ERREUR MODULE WALLET :", repr(exc))

print("")
print("=" * 70)
print("SERVICES GIFT RESELLERS")
print("=" * 70)

try:
    import gift_resellers.services as gs

    print("MODULE :", gs.__file__)

    for name in [
        "create_reseller_sale",
        "settle_reseller_sale",
        "create_sale_allocation",
        "calculate_reseller_sale_split",
    ]:
        fn = getattr(gs, name, None)

        if fn is None:
            print(f"\n{name} : INTROUVABLE")
        else:
            print(f"\n{name} :")
            print(inspect.signature(fn))

except Exception as exc:
    print("ERREUR MODULE REVENDEURS :", repr(exc))

print("")
print("=" * 70)
print("REGLES FINANCIERES EXISTANTES")
print("=" * 70)

try:
    from financial_routing.models import FinancialFeeRule

    for rule in FinancialFeeRule.objects.all().order_by("fee_type"):
        print(
            f"{rule.fee_type} | "
            f"{rule.percentage}% | "
            f"active={rule.active}"
        )
except Exception as exc:
    print("ERREUR REGLES FINANCIERES :", repr(exc))

print("")
print("=" * 70)
print("COMPTES FINANCIERS")
print("=" * 70)

try:
    from financial_accounts.models import FinancialAccount

    for account in FinancialAccount.objects.all().order_by("code"):
        print(
            f"{account.code} | "
            f"{account.name} | "
            f"type={account.account_type} | "
            f"currency={account.currency} | "
            f"status={account.status} | "
            f"balance={account.current_balance}"
        )
except Exception as exc:
    print("ERREUR COMPTES FINANCIERS :", repr(exc))

print("")
print("=" * 70)
print("INSPECTION STAGE 4 TERMINEE")
print("=" * 70)