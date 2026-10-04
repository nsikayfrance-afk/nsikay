import os
import sys

# Ajouter automatiquement le dossier backend au chemin Python.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from service_control.models import CountryServiceStatus


def afficher_etat():
    principaux = CountryServiceStatus.objects.filter(
        is_primary=True
    ).order_by("country_name")

    operationnels = principaux.filter(
        is_operational=True
    ).order_by("country_name")

    non_operationnels = principaux.filter(
        is_operational=False
    ).order_by("country_name")

    print("")
    print("=" * 70)
    print(" NSIKAY - ETAT DES PAYS OPERATIONNELS")
    print("=" * 70)
    print(f"PAYS ISO PRINCIPAUX       = {principaux.count()}")
    print(f"PAYS OPERATIONNELS        = {operationnels.count()}")
    print(f"PAYS NON OPERATIONNELS    = {non_operationnels.count()}")
    print("")

    print("PAYS OPERATIONNELS :")

    for country in operationnels:
        print(
            f"  {country.country_code} - "
            f"{country.country_name}"
        )

    print("")
    print("PAYS NON OPERATIONNELS :")

    for country in non_operationnels:
        print(
            f"  {country.country_code} - "
            f"{country.country_name}"
        )

    print("=" * 70)


def appliquer_liste(codes):
    codes = {
        str(code).strip().upper()
        for code in codes
        if str(code).strip()
    }

    print("")
    print("=" * 70)
    print(" VALIDATION DE LA LISTE OPERATIONNELLE")
    print("=" * 70)

    if len(codes) != 240:
        print(
            f"ERREUR : la liste contient {len(codes)} codes ISO3. "
            f"Elle doit contenir exactement 240 codes."
        )
        sys.exit(2)

    principaux = CountryServiceStatus.objects.filter(
        is_primary=True
    )

    principaux_codes = set(
        principaux.values_list("country_code", flat=True)
    )

    inconnus = sorted(codes - principaux_codes)

    if inconnus:
        print("ERREUR : codes ISO3 inconnus dans la liste :")

        for code in inconnus:
            print(f"  {code}")

        sys.exit(3)

    print("Liste valide : 240 codes ISO3 reconnus.")
    print("")

    # On ne touche qu'aux 249 lignes principales.
    # Les 125 doublons historiques restent inchanges.
    CountryServiceStatus.objects.filter(
        is_primary=True
    ).update(
        is_operational=False
    )

    CountryServiceStatus.objects.filter(
        is_primary=True,
        country_code__in=codes
    ).update(
        is_operational=True
    )

    operationnels = CountryServiceStatus.objects.filter(
        is_primary=True,
        is_operational=True
    ).count()

    print(
        f"PAYS OPERATIONNELS APRES APPLICATION = "
        f"{operationnels}"
    )

    if operationnels != 240:
        print(
            "ERREUR : le nombre final de pays operationnels "
            "n'est pas egal a 240."
        )
        sys.exit(4)

    print("")
    print("CONFIGURATION DES 240 PAYS OPERATIONNELS VALIDEE.")
    print("Aucune ligne historique n'a ete supprimee.")
    print("Aucune activation n'a ete supprimee.")
    print("=" * 70)


if __name__ == "__main__":

    if len(sys.argv) == 1:
        afficher_etat()
        sys.exit(0)

    appliquer_liste(sys.argv[1:])

