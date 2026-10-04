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

from django.urls import reverse

url = reverse(
    "service_dashboard:operational_countries"
)

print("ROUTE =", url)
print("ROUTE_OPERATIONAL_COUNTRIES = True")

