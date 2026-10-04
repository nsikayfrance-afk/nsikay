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

countries = (
    CountryServiceStatus.objects
    .filter(is_primary=True)
    .order_by("country_name")
)

output = os.path.join(
    BASE_DIR,
    "reports",
    "nsikay_249_pays_analyse.csv"
)

with open(
    output,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f, delimiter=";")

    writer.writerow([
        "NUMERO",
        "ISO3",
        "ISO2",
        "NUMERIQUE",
        "PAYS",
        "OPERATIONNEL_ACTUEL",
        "DECISION"
    ])

    for index, country in enumerate(countries, start=1):

        writer.writerow([
            index,
            country.country_code or "",
            country.iso2_code or "",
            country.iso_numeric_code or "",
            country.country_name,
            "OUI" if country.is_operational else "NON",
            ""
        ])

print("")
print("PAYS EXPORTES =", countries.count())
print("FICHIER =", output)

