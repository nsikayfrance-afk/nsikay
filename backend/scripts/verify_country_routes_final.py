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

routes = {
    "operational_countries":
        "service_dashboard:operational_countries",

    "operational_countries_history":
        "service_dashboard:operational_countries_history",
}

print("")
print("=" * 70)
print(" VERIFICATION ROUTES PAYS NSIKAY")
print("=" * 70)

for label, route_name in routes.items():

    url = reverse(route_name)

    print(
        label.upper(),
        "=",
        url
    )

print("=" * 70)

