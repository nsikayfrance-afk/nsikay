import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()

print("")
print("=" * 60)
print(" NSIKAY - TEST SERVICE DASHBOARD V7")
print("=" * 60)

user = User.objects.filter(
    is_superuser=True,
    is_active=True
).first()

if user is None:

    print("SUPERUSER=ABSENT")

else:

    print("SUPERUSER=", user.username)

    client = Client()
    client.force_login(user)

    routes = [
        "/service-dashboard/",
        "/service-dashboard/statistics/",
        "/service-dashboard/control-center/",
        "/service-dashboard/control-center-filtered/",
    ]

    results = []

    for route in routes:

        print("")
        print("-" * 60)
        print("ROUTE=", route)

        try:

            response = client.get(route)

            print("HTTP=", response.status_code)

            if response.status_code in (200, 201, 204):
                print("RESULT=OK")
                results.append(True)

            elif response.status_code in (301, 302, 303, 307, 308):
                print("RESULT=REDIRECTION")
                print("LOCATION=", response.get("Location"))
                results.append(False)

            elif response.status_code in (401, 403):
                print("RESULT=PROTECTION_OK")
                results.append(True)

            else:
                print("RESULT=ERREUR")
                results.append(False)

        except Exception as exc:

            print("RESULT=EXCEPTION")
            print("EXCEPTION_TYPE=", type(exc).__name__)
            print("EXCEPTION=", exc)
            results.append(False)

    print("")
    print("=" * 60)

    if all(results):
        print("SERVICE_DASHBOARD_ROUTES=OK")
    else:
        print("SERVICE_DASHBOARD_ROUTES=ERREUR")

print("=" * 60)
print(" TEST V7 TERMINE")
print("=" * 60)