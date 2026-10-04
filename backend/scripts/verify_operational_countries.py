import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from service_control.models import (
    CountryServiceStatus,
    GlobalService,
    ServiceActivation,
    ServiceRule,
)

print("")
print("=" * 70)
print(" CONTROLE FINAL - NSIKAY")
print("=" * 70)

print("SERVICES =", GlobalService.objects.count())
print("REGLES =", ServiceRule.objects.count())
print("LIGNES_PAYS =", CountryServiceStatus.objects.count())

print(
    "PAYS_ISO_PRINCIPAUX =",
    CountryServiceStatus.objects.filter(
        is_primary=True
    ).count()
)

print(
    "PAYS_OPERATIONNELS =",
    CountryServiceStatus.objects.filter(
        is_primary=True,
        is_operational=True
    ).count()
)

print(
    "PAYS_NON_OPERATIONNELS =",
    CountryServiceStatus.objects.filter(
        is_primary=True,
        is_operational=False
    ).count()
)

print(
    "ACTIVATIONS =",
    ServiceActivation.objects.count()
)

print("")
print("CONTROLE DE SECURITE :")

print(
    "LIGNES_HISTORIQUES_CONSERVEES =",
    CountryServiceStatus.objects.count() == 374
)

print(
    "ACTIVATIONS_CONSERVEES =",
    ServiceActivation.objects.count() == 10472
)

print(
    "ISO_PRINCIPAUX =",
    CountryServiceStatus.objects.filter(
        is_primary=True
    ).count() == 249
)

print(
    "240_PAYS_OPERATIONNELS =",
    CountryServiceStatus.objects.filter(
        is_primary=True,
        is_operational=True
    ).count() == 240
)

print("")
print("=" * 70)

