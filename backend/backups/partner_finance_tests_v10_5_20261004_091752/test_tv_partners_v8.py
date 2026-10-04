import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()

print("")
print("=" * 60)
print(" NSIKAY - TEST TV REGIE + PARTENAIRES V8")
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
        ("/dashboard/tv-regie/", "TV_REGIE_DASHBOARD"),
        ("/partners/dashboard/", "PARTNERS_DASHBOARD"),
        ("/partners/certification/", "PARTNERS_CERTIFICATION"),
        ("/partners/supply/", "PARTNERS_SUPPLY"),
    ]

    results = []

    for route, label in routes:

        print("")
        print("-" * 60)
        print("SERVICE=", label)
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

            elif response.status_code == 405:
                print("RESULT=METHODE_NON_AUTORISEE")
                results.append(False)

            elif response.status_code == 404:
                print("RESULT=404")
                results.append(False)

            else:
                print("RESULT=ERREUR_HTTP")
                results.append(False)

        except Exception as exc:

            print("RESULT=EXCEPTION")
            print("EXCEPTION_TYPE=", type(exc).__name__)
            print("EXCEPTION=", exc)
            results.append(False)

    print("")
    print("=" * 60)

    if all(results):
        print("TV_PARTNERS_ROUTES=OK")
    else:
        print("TV_PARTNERS_ROUTES=ANOMALIE")

print("=" * 60)
print(" TEST V8 TERMINE")
print("=" * 60)