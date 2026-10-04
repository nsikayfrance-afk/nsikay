from pathlib import Path
import inspect

from django.apps import apps

print("=" * 70)
print("MODELES GIFT RESELLERS")
print("=" * 70)

model_names = [
    "Reseller",
    "ResellerNetwork",
    "NetworkMember",
    "GiftInventoryUnit",
    "DistributionAgreement",
    "ResellerSale",
    "SaleAllocation",
    "GiftResellerAuditLog",
]

for name in model_names:
    try:
        model = apps.get_model("gift_resellers", name)
    except Exception as exc:
        print(f"\n{name}: ERREUR {exc}")
        continue

    print(f"\n--- {name} ---")
    print("TABLE :", model._meta.db_table)

    for field in model._meta.fields:
        print(
            f" - {field.name}"
            f" | type={field.__class__.__name__}"
            f" | null={field.null}"
            f" | blank={field.blank}"
            f" | default={field.default!r}"
        )

print("\n" + "=" * 70)
print("SERVICES.PY")
print("=" * 70)

service_path = Path("gift_resellers/services.py")
text = service_path.read_text(encoding="utf-8")
lines = text.splitlines()

keywords = [
    "def calculate",
    "def split",
    "def allocate",
    "def sell",
    "def create_reseller_sale",
    "def process",
    "ResellerSale.objects",
    "SaleAllocation.objects",
    "GiftResellerAuditLog.objects.create",
]

for i, line in enumerate(lines, 1):
    if any(k in line for k in keywords):
        start = max(1, i - 8)
        end = min(len(lines), i + 35)

        print(f"\n--- autour de la ligne {i} ---")
        for n in range(start, end + 1):
            print(f"{n:4}: {lines[n-1]}")

print("\n" + "=" * 70)
print("FONCTIONS DU MODULE")
print("=" * 70)

import gift_resellers.services as services

for name, obj in sorted(vars(services).items()):
    if callable(obj) and getattr(obj, "__module__", "") == services.__name__:
        try:
            signature = inspect.signature(obj)
        except Exception:
            signature = "(signature indisponible)"

        print(f"{name}{signature}")

print("\n" + "=" * 70)
print("MIGRATIONS")
print("=" * 70)

migration_dir = Path("gift_resellers/migrations")

for path in sorted(migration_dir.glob("*.py")):
    if path.name == "__init__.py":
        continue

    print(path.name)

print("\n" + "=" * 70)
print("INSPECTION STAGE 3 TERMINEE")
print("=" * 70)