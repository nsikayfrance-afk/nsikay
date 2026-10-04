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

from service_dashboard.models import (
    OperationalCountryConfigurationLog,
)

countries = CountryServiceStatus.objects.filter(
    is_primary=True
)

print("")
print("=" * 70)
print(" INTEGRITE NSIKAY APRES TRAÇABILITE")
print("=" * 70)

print(
    "LIGNES_PAYS =",
    CountryServiceStatus.objects.count()
)

print(
    "PAYS_ISO_PRINCIPAUX =",
    countries.count()
)

print(
    "PAYS_OPERATIONNELS =",
    countries.filter(
        is_operational=True
    ).count()
)

print(
    "ACTIVATIONS =",
    ServiceActivation.objects.count()
)

print(
    "JOURNAUX_CONFIGURATION =",
    OperationalCountryConfigurationLog.objects.count()
)

print("")
print(
    "374_LIGNES_CONSERVEES =",
    CountryServiceStatus.objects.count() == 374
)

print(
    "249_ISO_PRINCIPAUX =",
    countries.count() == 249
)

print(
    "10472_ACTIVATIONS_CONSERVEES =",
    ServiceActivation.objects.count() == 10472
)

print("=" * 70)

