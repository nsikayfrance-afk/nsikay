from django.apps import apps
from django.db import connection

print("=" * 70)
print(" NSIKAY - INSPECTION STAGE 4C")
print("=" * 70)

models_to_check = [
    ("gift_resellers", "Reseller"),
    ("gift_resellers", "ResellerNetwork"),
    ("gift_resellers", "NetworkMember"),
    ("gift_resellers", "GiftInventoryUnit"),
    ("gift_resellers", "DistributionAgreement"),
    ("gift_resellers", "ResellerSale"),
    ("gift_resellers", "SaleAllocation"),
    ("gift_resellers", "GiftResellerAuditLog"),
    ("financial_accounts", "GiftFinancialLedger"),
    ("finance", "WalletTransaction"),
]

for app_label, model_name in models_to_check:
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        print(f"\n{app_label}.{model_name} : ABSENT")
        continue

    print(f"\n{app_label}.{model_name}")
    print("-" * 60)

    for field in model._meta.fields:
        print(
            f" - {field.name}"
            f" | type={field.__class__.__name__}"
            f" | null={field.null}"
            f" | unique={field.unique}"
        )

    print("TABLE =", model._meta.db_table)

print("\n" + "=" * 70)
print(" CONTRAINTES")
print("=" * 70)

for app_label, model_name in models_to_check:
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        continue

    print(f"\n{app_label}.{model_name}")

    for constraint in model._meta.constraints:
        print(" -", constraint)

print("\n" + "=" * 70)
print(" FIN INSPECTION")
print("=" * 70)