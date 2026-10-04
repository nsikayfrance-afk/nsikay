from pathlib import Path

from django.apps import apps

print("=" * 70)
print("SERVICES.PY - LIGNES 1 A 210")
print("=" * 70)

path = Path("gift_resellers/services.py")
lines = path.read_text(encoding="utf-8").splitlines()

for i in range(1, min(211, len(lines) + 1)):
    print(f"{i:4}: {lines[i-1]}")

print("\n" + "=" * 70)
print("MODELE RESELLERSALE - VALIDATIONS / META")
print("=" * 70)

model = apps.get_model("gift_resellers", "ResellerSale")

print("\nTABLE :", model._meta.db_table)

for i, field in enumerate(model._meta.fields, 1):
    print(
        f"{i:2}. {field.name}"
        f" | {field.__class__.__name__}"
        f" | null={field.null}"
        f" | blank={field.blank}"
        f" | default={field.default!r}"
    )

print("\nCONTRAINTES :")
for constraint in model._meta.constraints:
    print(" -", constraint)

print("\nINDEXES :")
for index in model._meta.indexes:
    print(" -", index)

print("\nUNIQUE TOGETHER :", getattr(model._meta, "unique_together", None))

print("\n" + "=" * 70)
print("METHODES MODELE RESELLERSALE")
print("=" * 70)

for name in dir(model):
    if name.startswith("_"):
        continue

    attr = getattr(model, name, None)

    if callable(attr) and name in {
        "clean",
        "save",
        "full_clean",
    }:
        print("\n---", name, "---")
        try:
            import inspect
            print(inspect.getsource(attr))
        except Exception as exc:
            print("SOURCE INDISPONIBLE :", exc)

print("\n" + "=" * 70)
print("CHOIX STATUS RESELLERSALE")
print("=" * 70)

status_field = model._meta.get_field("status")

print(status_field.choices)

print("\n" + "=" * 70)
print("CHOIX SOURCE / STATUS GIFTINVENTORYUNIT")
print("=" * 70)

unit_model = apps.get_model("gift_resellers", "GiftInventoryUnit")

for field_name in ["source", "status", "credit_only"]:
    field = unit_model._meta.get_field(field_name)
    print(field_name, "=>", field.choices)

print("\n" + "=" * 70)
print("FIN INSPECTION COEUR STAGE 3")
print("=" * 70)