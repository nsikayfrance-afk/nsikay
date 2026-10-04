import os
import sys
import csv

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

import django
django.setup()

from service_control.models import CountryServiceStatus

countries = CountryServiceStatus.objects.filter(
    is_primary=True
).order_by("country_name")

output_file = os.path.join(
    BASE_DIR,
    "reports",
    "nsikay_249_pays_selection_240.csv"
)

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f, delimiter=";")

    writer.writerow([
        "ISO3",
        "ISO2",
        "NUMERIQUE",
        "PAYS",
        "OPERATIONNEL",
        "SELECTION_240"
    ])

    for country in countries:
        writer.writerow([
            country.country_code or "",
            country.iso2_code or "",
            country.iso_numeric_code or "",
            country.country_name,
            "OUI" if country.is_operational else "NON",
            ""
        ])

print("")
print("=" * 70)
print(" EXPORT PAYS PRINCIPAUX NSIKAY")
print("=" * 70)
print("PAYS EXPORTES =", countries.count())
print("FICHIER =", output_file)
print("")
print("Objectif operationnel = 240 pays")
print("Pays actuellement operationnels =", countries.filter(
    is_operational=True
).count())
print("Pays restant a selectionner =", 240 - countries.filter(
    is_operational=True
).count())
print("")
print("AUCUNE ACTIVATION MODIFIEE.")
print("=" * 70)

