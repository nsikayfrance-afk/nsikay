import os
import sys
import csv

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from service_control.models import CountryServiceStatus


# ============================================================
# ENTITES ISO MANIFESTEMENT NON-SOUVERAINES / TERRITORIALES
# ============================================================

TERRITORIES = {
    "ASM", "AIA", "ATA", "ABW", "BMU", "BES", "BVT",
    "IOT", "CYM", "CXR", "CCK", "COK", "CUW",
    "FLK", "FRO", "GUF", "PYF", "ATF", "GIB", "GRL",
    "GLP", "GUM", "GGY", "HMD", "HKG", "IMN", "JEY",
    "MAC", "MTQ", "MSR", "MYT", "NCL", "NIU", "NFK",
    "MNP", "PCN", "PRI", "REU", "BLM", "SHN", "MAF",
    "SPM", "SXM", "TCA", "TKL", "UMI", "VGB", "VIR",
    "WLF", "ESH", "ALA", "VAT", "SJM"
}

SPECIAL_CASES = {
    "PSE": "Etat observateur / statut politique particulier",
    "TWN": "Statut politique particulier",
    "ESH": "Territoire a statut particulier",
    "VAT": "Etat souverain particulier",
}

countries = (
    CountryServiceStatus.objects
    .filter(is_primary=True)
    .order_by("country_name")
)

rows = []

for index, country in enumerate(countries, start=1):

    iso3 = (country.country_code or "").upper()

    if iso3 in TERRITORIES:
        categorie = "TERRITOIRE_OU_ENTITE_ISO"
        proposition = "A_REVOIR"

    elif iso3 in SPECIAL_CASES:
        categorie = "CAS_PARTICULIER"
        proposition = "A_REVOIR"

    else:
        categorie = "ETAT_OU_ENTITE_A_CONSIDERER"
        proposition = "A_REVOIR"

    rows.append({
        "NUMERO": index,
        "ISO3": iso3,
        "ISO2": country.iso2_code or "",
        "NUMERIQUE": country.iso_numeric_code or "",
        "PAYS": country.country_name,
        "CATEGORIE": categorie,
        "DETAIL": SPECIAL_CASES.get(iso3, ""),
        "DECISION": "",
        "MOTIF": "",
    })


output = os.path.join(
    BASE_DIR,
    "reports",
    "nsikay_classification_249_entites.csv"
)

with open(
    output,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "NUMERO",
            "ISO3",
            "ISO2",
            "NUMERIQUE",
            "PAYS",
            "CATEGORIE",
            "DETAIL",
            "DECISION",
            "MOTIF",
        ],
        delimiter=";"
    )

    writer.writeheader()
    writer.writerows(rows)


print("")
print("TOTAL =", len(rows))

categories = {}

for row in rows:
    categories[row["CATEGORIE"]] = (
        categories.get(row["CATEGORIE"], 0) + 1
    )

print("")
print("REPARTITION :")

for key, value in categories.items():
    print(f"{key} = {value}")

print("")
print("TERRITOIRES / ENTITES ISO A REVOIR :")

for row in rows:
    if row["CATEGORIE"] == "TERRITOIRE_OU_ENTITE_ISO":
        print(
            f'{row["ISO3"]} | '
            f'{row["PAYS"]}'
        )

print("")
print("CAS PARTICULIERS :")

for row in rows:
    if row["CATEGORIE"] == "CAS_PARTICULIER":
        print(
            f'{row["ISO3"]} | '
            f'{row["PAYS"]} | '
            f'{row["DETAIL"]}'
        )

print("")
print("FICHIER =", output)

