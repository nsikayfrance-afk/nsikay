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

from service_control.models import (
    CountryServiceStatus,
    ServiceActivation,
)

primary = CountryServiceStatus.objects.filter(
    is_primary=True
)

operational = primary.filter(
    is_operational=True
)

print("")
print("=" * 70)
print(" CONTROLE BASE AVANT CONFIGURATION")
print("=" * 70)

print("LIGNES_PAYS =", CountryServiceStatus.objects.count())
print("PAYS_ISO_PRINCIPAUX =", primary.count())
print("PAYS_OPERATIONNELS =", operational.count())
print("ACTIVATIONS =", ServiceActivation.objects.count())

assert CountryServiceStatus.objects.count() == 374
assert primary.count() == 249
assert operational.count() == 0
assert ServiceActivation.objects.count() == 10472

print("")
print("BASE INTACTE = OK")
print("=" * 70)

