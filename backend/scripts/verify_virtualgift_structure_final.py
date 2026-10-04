import os
import sqlite3

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.conf import settings
from api_nsikay.models import VirtualGift

db = settings.DATABASES["default"]["NAME"]

expected = [
    "id",
    "name",
    "slug",
    "value",
    "currency",
    "value_eur",
    "currency_reference",
    "avatar",
    "category",
    "active",
    "display_order",
    "metadata",
]

connection = sqlite3.connect(db)
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(api_nsikay_virtualgift)")
rows = cursor.fetchall()

actual = [row[1] for row in rows]

print("")
print("=" * 70)
print(" NSIKAY - VERIFICATION STRUCTURE VIRTUALGIFT FINALE")
print("=" * 70)

print("")
print("BASE SQLITE :")
print(db)

print("")
print("===== COLONNES REELLES =====")

for row in rows:
    cid, name, field_type, notnull, default_value, pk = row

    print(
        f"{cid:02d} | "
        f"{name:25s} | "
        f"{field_type:20s} | "
        f"NOT NULL={notnull} | "
        f"DEFAULT={default_value} | "
        f"PK={pk}"
    )

print("")
print("===== COMPARAISON =====")

missing = [x for x in expected if x not in actual]
extra = [x for x in actual if x not in expected]

print("Colonnes attendues :", len(expected))
print("Colonnes réelles   :", len(actual))
print("Manquantes         :", missing if missing else "AUCUNE")
print("Supplémentaires    :", extra if extra else "AUCUNE")

print("")
print("Nombre de VirtualGift :", VirtualGift.objects.count())

print("")
if actual == expected:
    print("RESULTAT : STRUCTURE COMPLETE ET DANS L'ORDRE ATTENDU")
elif not missing and not extra:
    print("RESULTAT : STRUCTURE COMPLETE")
else:
    print("RESULTAT : VERIFICATION NECESSAIRE")

connection.close()

print("")
print("=" * 70)