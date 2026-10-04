import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.urls import reverse, resolve

print("")
print("=" * 70)
print(" VERIFICATION ROUTE PAYS OPERATIONNELS")
print("=" * 70)

url = reverse("operational_countries")

print("NOM ROUTE      =", "operational_countries")
print("URL RESOLUE     =", url)

match = resolve(url)

print(
    "VUE RESOLUE     =",
    match.func.__module__,
    ".",
    match.func.__name__,
    sep=""
)

print("")
print("ROUTE_OPERATIONAL_COUNTRIES = True")
print("=" * 70)

