import os
import sys
import traceback

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

print("=" * 70)
print(" NSIKAY - DIAGNOSTIC E2E GLOBAL READ-ONLY")
print("=" * 70)
print()

# ----------------------------------------------------------------------
# 1. DJANGO SETUP
# ----------------------------------------------------------------------
try:
    import django
    print(f"[DJANGO] version = {django.get_version()}")
    django.setup()
    print("[DJANGO] django.setup() = OK")
except Exception as e:
    print("[DJANGO] ERREUR")
    print(type(e).__name__, str(e))
    traceback.print_exc()
    sys.exit(1)

from django.conf import settings
from django.apps import apps
from django.db import connection
from django.core.management import call_command

# ----------------------------------------------------------------------
# 2. SETTINGS
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("1. CONFIGURATION")
print("-" * 70)

print("DEBUG =", getattr(settings, "DEBUG", None))
print("DATABASE ENGINE =", settings.DATABASES["default"].get("ENGINE"))
print("DATABASE NAME =", settings.DATABASES["default"].get("NAME"))
print("DATABASE HOST =", settings.DATABASES["default"].get("HOST"))
print("DATABASE PORT =", settings.DATABASES["default"].get("PORT"))

# ----------------------------------------------------------------------
# 3. DJANGO CHECK
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("2. DJANGO CHECK")
print("-" * 70)

try:
    call_command("check", verbosity=1)
    print("[CHECK] OK")
except Exception as e:
    print("[CHECK] ERREUR :", type(e).__name__, str(e))

# ----------------------------------------------------------------------
# 4. MIGRATIONS
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("3. MIGRATIONS")
print("-" * 70)

try:
    call_command("showmigrations", verbosity=1)
except Exception as e:
    print("[MIGRATIONS] ERREUR :", type(e).__name__, str(e))

print()
print("---- MIGRATIONS NON APPLIQUEES ----")

try:
    from io import StringIO
    output = StringIO()
    call_command("showmigrations", "--plan", stdout=output, stderr=output)
    plan = output.getvalue()

    pending = []
    for line in plan.splitlines():
        if "[ ]" in line:
            pending.append(line)

    if pending:
        for line in pending:
            print(line)
        print("TOTAL PENDING =", len(pending))
    else:
        print("AUCUNE MIGRATION NON APPLIQUEE")
except Exception as e:
    print("[MIGRATION PLAN] ERREUR :", type(e).__name__, str(e))

# ----------------------------------------------------------------------
# 5. APPLICATIONS
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("4. APPLICATIONS DJANGO")
print("-" * 70)

for config in apps.get_app_configs():
    print(
        f"{config.label:35} "
        f"name={config.name}"
    )

# ----------------------------------------------------------------------
# 6. MODELES
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("5. MODELES DJANGO")
print("-" * 70)

model_count = 0

for model in apps.get_models():
    model_count += 1
    print(
        f"{model._meta.label:45} "
        f"table={model._meta.db_table}"
    )

print()
print("TOTAL MODELES =", model_count)

# ----------------------------------------------------------------------
# 7. DETECTION DES MODELES ENREGISTRES PLUSIEURS FOIS
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("6. DETECTION DOUBLONS MODELES")
print("-" * 70)

model_labels = {}

for model in apps.get_models():
    label = model._meta.label
    model_labels.setdefault(label, []).append(model)

duplicates = {
    label: models
    for label, models in model_labels.items()
    if len(models) > 1
}

if duplicates:
    print("DOUBLONS DETECTES :")
    for label, models in duplicates.items():
        print(" ", label, "=>", len(models))
        for model in models:
            print(
                "      ",
                model,
                "table=",
                model._meta.db_table
            )
else:
    print("AUCUN DOUBLON DANS apps.get_models()")

# Recherche spécifique FinancialOperation
print()
print("RECHERCHE SPECIFIQUE : finance.FinancialOperation")

matches = []

for model in apps.get_models():
    if (
        model.__name__.lower() == "financialoperation"
        or model._meta.label.lower() == "finance.financialoperation"
    ):
        matches.append(model)

if matches:
    for i, model in enumerate(matches, 1):
        print(
            f"  #{i}",
            model,
            "label=",
            model._meta.label,
            "table=",
            model._meta.db_table,
            "module=",
            model.__module__
        )
else:
    print("  Aucun modèle FinancialOperation trouvé.")

# ----------------------------------------------------------------------
# 8. TABLES POSTGRESQL
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("7. INVENTAIRE TABLES POSTGRESQL")
print("-" * 70)

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)
    tables = [row[0] for row in cursor.fetchall()]

print("TOTAL TABLES =", len(tables))

# Affichage ciblé
interesting_prefixes = (
    "events_",
    "media_",
    "wallet_",
    "finance_",
    "banking_",
    "wenze_",
    "certification_",
    "administration_",
    "api_",
)

for prefix in interesting_prefixes:
    selected = [t for t in tables if t.startswith(prefix)]

    print()
    print(f"[{prefix}] {len(selected)} tables")

    for table in selected:
        print(" ", table)

# ----------------------------------------------------------------------
# 9. TABLES ATTENDUES PAR LES MODELES MAIS ABSENTES
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("8. MODELES -> TABLES MANQUANTES")
print("-" * 70)

missing_tables = []

with connection.cursor() as cursor:
    for model in apps.get_models():
        table = model._meta.db_table

        try:
            cursor.execute(
                """
                SELECT to_regclass(%s)
                """,
                [f"public.{table}"]
            )

            result = cursor.fetchone()[0]

            if result is None:
                missing_tables.append(
                    (
                        model._meta.label,
                        table
                    )
                )
        except Exception as e:
            print(
                "ERREUR VERIFICATION TABLE",
                model._meta.label,
                table,
                type(e).__name__,
                str(e)
            )

if missing_tables:
    print("TABLES MANQUANTES DETECTEES :")
    for label, table in missing_tables:
        print(
            f"  MODEL={label:45} TABLE={table}"
        )
else:
    print("AUCUNE TABLE MANQUANTE POUR LES MODELES DJANGO")

# ----------------------------------------------------------------------
# 10. CAS SPECIFIQUE EVENTS
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("9. DIAGNOSTIC SPECIFIQUE EVENTS")
print("-" * 70)

event_models = []

for model in apps.get_models():
    if model._meta.db_table.startswith("events_"):
        event_models.append(model)

print("MODELES events_* :")

if event_models:
    for model in event_models:
        print(
            " ",
            model._meta.label,
            "->",
            model._meta.db_table
        )
else:
    print("  Aucun modèle avec table events_*")

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
          AND tablename LIKE 'events_%'
        ORDER BY tablename
    """)

    event_tables = [row[0] for row in cursor.fetchall()]

print()
print("TABLES PostgreSQL events_* :")

if event_tables:
    for table in event_tables:
        print(" ", table)
else:
    print("  AUCUNE")

target = "events_eventregistration"

with connection.cursor() as cursor:
    cursor.execute(
        "SELECT to_regclass(%s)",
        [f"public.{target}"]
    )
    target_exists = cursor.fetchone()[0]

print()
print(
    "events_eventregistration =",
    target_exists
)

if target_exists is None:
    print(
        "RESULTAT : table absente de PostgreSQL."
    )

# ----------------------------------------------------------------------
# 11. TABLES MEDIA EVENT REGISTRATION
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("10. EVENT REGISTRATION ACTUEL")
print("-" * 70)

for table in (
    "media_eventregistration",
    "events_eventregistration",
):

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT to_regclass(%s)",
            [f"public.{table}"]
        )

        exists = cursor.fetchone()[0]

    print(
        f"{table:35} -> {exists}"
    )

# ----------------------------------------------------------------------
# 12. UTILISATEURS ACTUELS
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("11. UTILISATEURS")
print("-" * 70)

try:
    from django.contrib.auth import get_user_model

    User = get_user_model()

    users = User.objects.all().order_by("id")

    print("TOTAL USERS =", users.count())

    for user in users:
        print(
            f"ID={user.id:<4} "
            f"username={user.username:<45} "
            f"staff={user.is_staff} "
            f"superuser={user.is_superuser} "
            f"active={user.is_active}"
        )
except Exception as e:
    print("[USERS] ERREUR :", type(e).__name__, str(e))

# ----------------------------------------------------------------------
# 13. VERIFICATION ABSENCE E2E
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("12. VERIFICATION COMPTES E2E")
print("-" * 70)

try:
    e2e_users = User.objects.filter(
        username__startswith="NSIKAY_E2E_"
    )

    print(
        "COMPTES NSIKAY_E2E_* =",
        e2e_users.count()
    )

    for user in e2e_users:
        print(
            " ",
            user.id,
            user.username
        )
except Exception as e:
    print("[E2E USERS] ERREUR :", type(e).__name__, str(e))

# ----------------------------------------------------------------------
# 14. WALLET E2E
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("13. VERIFICATION WALLETS E2E")
print("-" * 70)

wallet_tables = [
    "wallet_wallet",
    "finance_wallet",
]

with connection.cursor() as cursor:

    for table in wallet_tables:

        cursor.execute(
            "SELECT to_regclass(%s)",
            [f"public.{table}"]
        )

        exists = cursor.fetchone()[0]

        print(
            f"{table:30} -> {exists}"
        )

        if exists:
            try:
                cursor.execute(
                    f"SELECT COUNT(*) FROM {table}"
                )

                count = cursor.fetchone()[0]

                print(
                    f"  ROW COUNT = {count}"
                )
            except Exception as e:
                print(
                    "  COUNT ERROR:",
                    type(e).__name__,
                    str(e)
                )

# ----------------------------------------------------------------------
# 15. MIGRATION TABLE DJANGO
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("14. ETAT DJANGO MIGRATIONS")
print("-" * 70)

try:
    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT app, name
            FROM django_migrations
            ORDER BY app, applied
        """)

        migrations = cursor.fetchall()

    print(
        "MIGRATIONS ENREGISTREES =",
        len(migrations)
    )

    apps_migrations = {}

    for app, name in migrations:
        apps_migrations.setdefault(app, 0)
        apps_migrations[app] += 1

    for app, count in sorted(apps_migrations.items()):
        print(
            f"  {app:35} {count}"
        )

except Exception as e:
    print(
        "[DJANGO MIGRATIONS] ERREUR:",
        type(e).__name__,
        str(e)
    )

# ----------------------------------------------------------------------
# 16. FKS CIBLANT AUTH_USER
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("15. FOREIGN KEYS -> AUTH_USER")
print("-" * 70)

with connection.cursor() as cursor:

    cursor.execute("""
        SELECT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name,
            rc.delete_rule
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
         AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
         AND ccu.table_schema = tc.table_schema
        JOIN information_schema.referential_constraints AS rc
          ON rc.constraint_name = tc.constraint_name
         AND rc.constraint_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND ccu.table_name = 'auth_user'
        ORDER BY tc.table_name, kcu.column_name
    """)

    fks = cursor.fetchall()

print("TOTAL FKs -> auth_user =", len(fks))

for table, column, foreign_table, foreign_column, delete_rule in fks:
    print(
        f"{table:50} "
        f"{column:35} "
        f"ON DELETE {delete_rule}"
    )

# ----------------------------------------------------------------------
# 17. TABLES AVEC ZERO ROWS
# ----------------------------------------------------------------------
print()
print("-" * 70)
print("16. TABLES VIDES IMPORTANTES")
print("-" * 70)

important_prefixes = (
    "association_",
    "certification_",
    "banking_",
    "finance_",
    "wallet_",
    "wenze_",
    "media_",
    "api_",
)

empty_tables = []

with connection.cursor() as cursor:

    for table in tables:

        if not table.startswith(important_prefixes):
            continue

        try:
            cursor.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            )

            count = cursor.fetchone()[0]

            if count == 0:
                empty_tables.append(table)

        except Exception:
            pass

print(
    "TABLES VIDES DETECTEES =",
    len(empty_tables)
)

for table in empty_tables:
    print(" ", table)

# ----------------------------------------------------------------------
# 18. RESUME
# ----------------------------------------------------------------------
print()
print("=" * 70)
print(" RESUME DIAGNOSTIC")
print("=" * 70)

print(
    "Django setup              : OK"
)

print(
    "Modeles Django            :",
    model_count
)

print(
    "Tables PostgreSQL         :",
    len(tables)
)

print(
    "Tables modeles manquantes :",
    len(missing_tables)
)

print(
    "Doublons modeles          :",
    len(duplicates)
)

print(
    "Tables events_*            :",
    len(event_tables)
)

print(
    "Compte E2E restant        :",
    (
        e2e_users.count()
        if "e2e_users" in locals()
        else "N/A"
    )
)

print()
print("=" * 70)
print(" FIN DU DIAGNOSTIC - AUCUNE MODIFICATION EFFECTUEE")
print("=" * 70)
