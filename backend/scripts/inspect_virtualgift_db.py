import os
import sqlite3

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.conf import settings
from api_nsikay.models import VirtualGift

db = settings.DATABASES["default"]["NAME"]

print("")
print("=" * 70)
print(" NSIKAY - INSPECTION REELLE TABLE VIRTUALGIFT")
print("=" * 70)

print("")
print("BASE DE DONNEES :")
print(db)

print("")
print("===== COLONNES SQLITE =====")

connection = sqlite3.connect(db)
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(api_nsikay_virtualgift)")
columns = cursor.fetchall()

for row in columns:
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
print("===== MODELE DJANGO =====")

for field in VirtualGift._meta.fields:
    print(
        f"{field.name:25s} | "
        f"{field.__class__.__name__:25s} | "
        f"default={field.default!r}"
    )

print("")
print("===== NOMBRE DE CADEAUX =====")

print("VirtualGift.objects.count() =", VirtualGift.objects.count())

connection.close()

print("")
print("=" * 70)
print(" FIN INSPECTION")
print("=" * 70)