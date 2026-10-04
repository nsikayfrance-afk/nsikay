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

from service_dashboard.operational_countries_views import (
    operational_countries
)

print("")
print("=" * 70)
print(" VERIFICATION VUE")
print("=" * 70)

print("MODULE =", operational_countries.__module__)
print("FONCTION =", operational_countries.__name__)
print("VUE_OPERATIONAL_COUNTRIES = True")

print("=" * 70)

