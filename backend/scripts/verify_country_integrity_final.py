import os
import sys

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

from service_control.models import (
    CountryServiceStatus,
    ServiceActivation,
)

countries = CountryServiceStatus.objects.filter(
    is_primary=True
)

print("LIGNES_PAYS =", CountryServiceStatus.objects.count())
print("PAYS_ISO_PRINCIPAUX =", countries.count())
print(
    "PAYS_OPERATIONNELS =",
    countries.filter(is_operational=True).count()
)
print(
    "ACTIVATIONS =",
    ServiceActivation.objects.count()
)

