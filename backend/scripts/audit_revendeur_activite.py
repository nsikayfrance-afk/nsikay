import os
import sys

# Force le dossier backend dans Python
BACKEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND not in sys.path:
    sys.path.insert(0, BACKEND)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import connection

print("=" * 70)
print("1. DJANGO")
print("=" * 70)
print("BACKEND :", BACKEND)
print("DJANGO  :", django.get_version())

print("")
print("=" * 70)
print("2. MODELES GIFT_RESELLERS")
print("=" * 70)

try:
    app = apps.get_app_config("gift_resellers")

    for model in app.get_models():
        print(f"\nMODEL : {model._meta.label}")
        print(f"TABLE : {model._meta.db_table}")

        for f in model._meta.fields:
            remote = getattr(getattr(f, "remote_field", None), "model", None)

            print(
                f"  FIELD {f.name:<30} "
                f"type={f.__class__.__name__:<22} "
                f"null={getattr(f,'null',None)} "
                f"related={remote}"
            )

except Exception as e:
    print("ERREUR gift_resellers :", repr(e))

print("")
print("=" * 70)
print("3. MODELES NSIKAY_ACTIVITIES")
print("=" * 70)

try:
    app = apps.get_app_config("nsikay_activities")

    for model in app.get_models():
        print(f"\nMODEL : {model._meta.label}")
        print(f"TABLE : {model._meta.db_table}")

        for f in model._meta.fields:
            remote = getattr(getattr(f, "remote_field", None), "model", None)

            print(
                f"  FIELD {f.name:<30} "
                f"type={f.__class__.__name__:<22} "
                f"null={getattr(f,'null',None)} "
                f"related={remote}"
            )

except Exception as e:
    print("ERREUR nsikay_activities :", repr(e))

print("")
print("=" * 70)
print("4. ACTIVITY / TYPES D'ACTIVITE")
print("=" * 70)

try:
    from nsikay_activities.models import Activity

    print("Activity :", Activity)
    print("TABLE    :", Activity._meta.db_table)

    try:
        field = Activity._meta.get_field("activity_type")
        print("activity_type choices :", getattr(field, "choices", None))
    except Exception as e:
        print("activity_type absent :", repr(e))

    print("")
    print("Nombre total activités :", Activity.objects.count())

    from django.db.models import Count

    rows = (
        Activity.objects
        .values("activity_type")
        .annotate(total=Count("id"))
        .order_by("activity_type")
    )

    for row in rows:
        print(" ", row)

except Exception as e:
    print("ERREUR Activity :", repr(e))

print("")
print("=" * 70)
print("5. MODELES CONTENANT REVENDEUR / CADEAU / GIFT")
print("=" * 70)

keywords = (
    "reseller",
    "giftreseller",
    "gift_reseller",
    "revendeur",
    "cadeau",
    "gift",
)

for app_config in apps.get_app_configs():

    for model in app_config.get_models():

        searchable = (
            model.__name__
            + " "
            + model._meta.label
            + " "
            + " ".join(f.name for f in model._meta.fields)
        ).lower()

        if any(k in searchable for k in keywords):

            print(f"\nMATCH : {model._meta.label}")
            print("TABLE :", model._meta.db_table)

            for f in model._meta.fields:

                remote = getattr(
                    getattr(f, "remote_field", None),
                    "model",
                    None
                )

                print(
                    f"  {f.name:<30} "
                    f"{f.__class__.__name__:<22} "
                    f"related={remote}"
                )

print("")
print("=" * 70)
print("6. RELATIONS DIRECTES VERS Activity")
print("=" * 70)

try:
    from nsikay_activities.models import Activity

    found = False

    for app_config in apps.get_app_configs():

        for model in app_config.get_models():

            for f in model._meta.fields:

                remote = getattr(
                    getattr(f, "remote_field", None),
                    "model",
                    None
                )

                if remote is Activity:
                    found = True
                    print(
                        f"{model._meta.label}.{f.name}"
                        f" -> Activity"
                    )

    if not found:
        print("Aucune relation directe trouvée.")

except Exception as e:
    print("ERREUR relations Activity :", repr(e))

print("")
print("=" * 70)
print("7. RELATIONS VERS USER")
print("=" * 70)

User = get_user_model()

for app_config in apps.get_app_configs():

    for model in app_config.get_models():

        for f in model._meta.fields:

            remote = getattr(
                getattr(f, "remote_field", None),
                "model",
                None
            )

            if remote is User:
                print(
                    f"{model._meta.label}.{f.name}"
                    f" -> User"
                )

print("")
print("=" * 70)
print("8. TABLES SQL GIFT / RESELLER / CADEAU")
print("=" * 70)

with connection.cursor() as cursor:

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND (
              table_name ILIKE '%gift%'
              OR table_name ILIKE '%resell%'
              OR table_name ILIKE '%cadeau%'
          )
        ORDER BY table_name
    """)

    rows = cursor.fetchall()

    if not rows:
        print("Aucune table trouvée.")

    for row in rows:
        print(row[0])

print("")
print("=" * 70)
print("9. FIN AUDIT")
print("AUCUNE MODIFICATION FONCTIONNELLE")
print("=" * 70)
