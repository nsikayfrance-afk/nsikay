import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()

print("")
print("=" * 60)
print(" NSIKAY - TEST CONTROL CENTER V5")
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
        "/service-dashboard/control-center-filtered/",
    ]

    for route in routes:

        print("")
        print("-" * 60)
        print("ROUTE=", route)

        try:

            response = client.get(route)

            print("HTTP=", response.status_code)

            if response.status_code in (200, 201, 204):
                print("RESULT=OK")

            elif response.status_code in (301, 302, 303, 307, 308):
                print("RESULT=REDIRECTION")
                print("LOCATION=", response.get("Location"))

            elif response.status_code in (401, 403):
                print("RESULT=PROTECTION_OK")

            elif response.status_code >= 500:
                print("RESULT=ERREUR_SERVEUR")

            else:
                print("RESULT=HTTP_NON_ATTENDU")

        except Exception as exc:

            print("RESULT=EXCEPTION")
            print("EXCEPTION_TYPE=", type(exc).__name__)
            print("EXCEPTION=", exc)

print("")
print("=" * 60)
print(" TEST CONTROL CENTER V5 TERMINE")
print("=" * 60)