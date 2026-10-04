import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from service_control.models import CountryServiceStatus, ServiceActivation

EXCLUDED = {
    "ATA",
    "BVT",
    "IOT",
    "ATF",
    "HMD",
    "PCN",
    "SGS",
    "UMI",
    "SJM",
}

primary = CountryServiceStatus.objects.filter(is_primary=True)

expected_operational = set(
    primary.values_list("country_code", flat=True)
) - EXCLUDED

actual_operational = set(
    primary.filter(is_operational=True)
    .values_list("country_code", flat=True)
)

actual_excluded = set(
    primary.filter(is_operational=False)
    .values_list("country_code", flat=True)
)

print("")
print("=" * 70)
print(" VERIFICATION EXACTE DES 240 PAYS")
print("=" * 70)

print("PAYS PRINCIPAUX :", primary.count())
print("ATTENDUS OPERATIONNELS :", len(expected_operational))
print("ACTUELS OPERATIONNELS :", len(actual_operational))
print("ATTENDUS EXCLUS :", len(EXCLUDED))
print("ACTUELS EXCLUS :", len(actual_excluded))
print("ACTIVATIONS :", ServiceActivation.objects.count())

if actual_operational != expected_operational:
    missing = sorted(expected_operational - actual_operational)
    extra = sorted(actual_operational - expected_operational)

    print("")
    print("PAYS MANQUANTS :", missing)
    print("PAYS ACTIVÉS PAR ERREUR :", extra)

    raise SystemExit(
        "ECHEC : les 240 pays ne correspondent pas exactement."
    )

if actual_excluded != EXCLUDED:
    raise SystemExit(
        "ECHEC : les 9 exclusions ne correspondent pas exactement."
    )

if primary.count() != 249:
    raise SystemExit("ECHEC : 249 pays principaux attendus.")

if len(actual_operational) != 240:
    raise SystemExit("ECHEC : exactement 240 pays attendus.")

if len(actual_excluded) != 9:
    raise SystemExit("ECHEC : exactement 9 exclusions attendues.")

if ServiceActivation.objects.count() != 10472:
    raise SystemExit(
        "ECHEC : les 10 472 activations doivent rester intactes."
    )

print("")
print("RESULTAT = OK")
print("")
print("249 pays principaux")
print("240 pays operationnels")
print("9 pays exclus")
print("10 472 ServiceActivation conservees")
print("")
print("CONFIGURATION DES 240 PAYS VALIDEE.")
print("=" * 70)

