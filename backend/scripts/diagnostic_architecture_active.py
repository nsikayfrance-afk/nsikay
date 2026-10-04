import os
import sys
import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

print("=" * 78)
print(" NSIKAY - AUDIT ARCHITECTURE ACTIVE")
print("=" * 78)
print(f"ROOT     : {ROOT}")
print(f"PYTHON   : {sys.version}")
print()

# ---------------------------------------------------------------------
# 1. DJANGO
# ---------------------------------------------------------------------
print("=" * 78)
print("1. DJANGO / CONFIGURATION")
print("=" * 78)

try:
    import django
    print("Django :", django.get_version())
    django.setup()
    print("django.setup() : OK")
except Exception as exc:
    print("DJANGO ERROR :", repr(exc))
    sys.exit(1)

from django.conf import settings
from django.apps import apps
from django.db import connection
from django.core.management import call_command

print("SETTINGS_MODULE :", os.environ.get("DJANGO_SETTINGS_MODULE"))
print("DATABASE ENGINE :", settings.DATABASES["default"]["ENGINE"])
print("DATABASE NAME   :", settings.DATABASES["default"].get("NAME"))
print()

# ---------------------------------------------------------------------
# 2. MANAGE.PY CHECK
# ---------------------------------------------------------------------
print("=" * 78)
print("2. MANAGE.PY CHECK")
print("=" * 78)

try:
    call_command("check", verbosity=1)
except Exception as exc:
    print("CHECK ERROR :", repr(exc))

print()

# ---------------------------------------------------------------------
# 3. INSTALLED APPS
# ---------------------------------------------------------------------
print("=" * 78)
print("3. INSTALLED APPS")
print("=" * 78)

for app in settings.INSTALLED_APPS:
    print(app)

print()

# ---------------------------------------------------------------------
# 4. ACTIVE DJANGO APP REGISTRY
# ---------------------------------------------------------------------
print("=" * 78)
print("4. MODELES ACTUELLEMENT ENREGISTRES PAR DJANGO")
print("=" * 78)

for model in sorted(apps.get_models(), key=lambda m: (
    m._meta.app_label,
    m._meta.model_name
)):
    print(
        f"{model._meta.app_label:30} "
        f"{model.__name__:35} "
        f"table={model._meta.db_table}"
    )

print()

# ---------------------------------------------------------------------
# 5. PROFILE MODELS
# ---------------------------------------------------------------------
print("=" * 78)
print("5. MODELES DE PROFILS")
print("=" * 78)

profile_models = []

for model in apps.get_models():
    name = model.__name__.lower()
    table = model._meta.db_table.lower()

    if (
        "profile" in name
        or "profile" in table
        or model._meta.app_label in {
            "core",
            "nsikay_profiles",
            "nsikay_activities",
        }
    ):
        profile_models.append(model)

for model in sorted(profile_models, key=lambda m: (
    m._meta.app_label,
    m.__name__
)):
    print()
    print(
        f"{model._meta.app_label}.{model.__name__}"
        f"  TABLE={model._meta.db_table}"
    )

    for field in model._meta.fields:
        print(
            f"    FIELD {field.name:30} "
            f"type={field.__class__.__name__:25} "
            f"null={field.null} "
            f"blank={getattr(field, 'blank', None)}"
        )

        if getattr(field, "choices", None):
            print("      choices:")
            for choice in field.choices:
                print("        ", choice)

print()

# ---------------------------------------------------------------------
# 6. URLS
# ---------------------------------------------------------------------
print("=" * 78)
print("6. ROUTES DJANGO")
print("=" * 78)

def show_urls(patterns, prefix=""):
    for pattern in patterns:
        route = getattr(pattern, "_route", "")
        current = prefix + route

        callback = getattr(pattern, "callback", None)
        callback_name = ""

        if callback is not None:
            callback_name = getattr(callback, "__qualname__", repr(callback))

        print(f"{current:65} {callback_name}")

        nested = getattr(pattern, "url_patterns", None)
        if nested:
            show_urls(nested, current)

try:
    from nsikay.urls import urlpatterns
    show_urls(urlpatterns)
except Exception as exc:
    print("URL ERROR :", repr(exc))

print()

# ---------------------------------------------------------------------
# 7. DATABASE TABLES
# ---------------------------------------------------------------------
print("=" * 78)
print("7. TABLES POSTGRESQL CIBLEES")
print("=" * 78)

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = [row[0] for row in cursor.fetchall()]

interesting_prefixes = (
    "core_",
    "nsikay_profiles_",
    "nsikay_activities_",
    "business_",
    "certification_",
    "administration_",
    "api_",
    "finance_",
    "wallet_",
    "banking_",
    "wenze_",
    "media_",
    "tv_",
    "events_",
)

for table in tables:
    if table.startswith(interesting_prefixes):
        print(table)

print()

# ---------------------------------------------------------------------
# 8. MODEL -> TABLE EXISTENCE
# ---------------------------------------------------------------------
print("=" * 78)
print("8. MODELES DJANGO DONT LA TABLE N'EXISTE PAS")
print("=" * 78)

db_tables = set(tables)

for model in sorted(apps.get_models(), key=lambda m: (
    m._meta.app_label,
    m.__name__
)):
    table = model._meta.db_table

    if table not in db_tables:
        print(
            f"MISSING TABLE : "
            f"{model._meta.app_label}.{model.__name__} -> {table}"
        )

print()

# ---------------------------------------------------------------------
# 9. SPECIFIC PROFILE TABLES
# ---------------------------------------------------------------------
print("=" * 78)
print("9. TABLES PROFILS")
print("=" * 78)

for table in sorted(db_tables):
    if "profile" in table.lower():
        print(table)

print()

# ---------------------------------------------------------------------
# 10. EVENTS / MEDIA REGISTRATION
# ---------------------------------------------------------------------
print("=" * 78)
print("10. EVENTS / MEDIA EVENT REGISTRATION")
print("=" * 78)

print("Django models:")
for model in apps.get_models():
    table = model._meta.db_table.lower()
    if "eventregistration" in table or table.startswith("events_"):
        print(
            f"  {model._meta.app_label}.{model.__name__}"
            f" -> {model._meta.db_table}"
        )

print("PostgreSQL:")
for table in sorted(db_tables):
    if table.startswith("events_") or "eventregistration" in table:
        print(" ", table)

print()

# ---------------------------------------------------------------------
# 11. DUPLICATE MODEL CLASSES / FINANCIAL OPERATION
# ---------------------------------------------------------------------
print("=" * 78)
print("11. FINANCIAL OPERATION / MODELES FINANCIERS")
print("=" * 78)

for model in apps.get_models():
    if model.__name__.lower() in {
        "financialoperation",
        "financialtransaction",
        "wallet",
        "wallettransaction",
    }:
        print(
            f"{model._meta.app_label}.{model.__name__}"
            f" -> {model._meta.db_table}"
        )

print()

# ---------------------------------------------------------------------
# 12. ACTIVE SOURCE FILES
# ---------------------------------------------------------------------
print("=" * 78)
print("12. FICHIERS SOURCE ACTIFS - PROFILS / ACTIVITES")
print("=" * 78)

ACTIVE_EXTENSIONS = {".py", ".jsx", ".js", ".ts", ".tsx"}

def is_ignored(path):
    parts = {p.lower() for p in path.parts}

    if "__pycache__" in parts:
        return True

    if "backups" in parts:
        return True

    if ".git" in parts:
        return True

    if "node_modules" in parts:
        return True

    return False

keywords = (
    "profile",
    "activity",
    "activities",
    "metier",
    "engagement",
    "invitation",
)

for base in [ROOT / "backend", ROOT / "frontend" / "src"]:
    if not base.exists():
        continue

    for path in base.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in ACTIVE_EXTENSIONS:
            continue

        if is_ignored(path):
            continue

        lower = path.name.lower()

        if any(keyword in lower for keyword in keywords):
            print(path.relative_to(ROOT))

print()

# ---------------------------------------------------------------------
# 13. PROFILE CREATION IN ACTIVE PYTHON SOURCE
# ---------------------------------------------------------------------
print("=" * 78)
print("13. CREATIONS DE PROFILS DANS LE CODE ACTIF")
print("=" * 78)

targets = (
    "NsikayProfile.objects.create",
    "NsikayProfile.objects.get_or_create",
    "Profile.objects.create",
    "Profile.objects.get_or_create",
    "profile_type",
)

for path in (ROOT / "backend").rglob("*.py"):
    if is_ignored(path):
        continue

    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        continue

    hits = []

    for lineno, line in enumerate(text.splitlines(), 1):
        if any(target in line for target in targets):
            hits.append((lineno, line.strip()))

    if hits:
        print()
        print(path.relative_to(ROOT))
        for lineno, line in hits:
            print(f"  {lineno}: {line}")

print()

# ---------------------------------------------------------------------
# 14. PROFILE IMPORTS
# ---------------------------------------------------------------------
print("=" * 78)
print("14. IMPORTS DES SYSTEMES DE PROFILS")
print("=" * 78)

for path in (ROOT / "backend").rglob("*.py"):
    if is_ignored(path):
        continue

    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        continue

    hits = []

    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()

        if (
            "nsikay_profiles" in stripped
            or "core.models" in stripped
            or "NsikayProfile" in stripped
        ):
            hits.append((lineno, stripped))

    if hits:
        print()
        print(path.relative_to(ROOT))
        for lineno, line in hits:
            print(f"  {lineno}: {line}")

print()

# ---------------------------------------------------------------------
# 15. SERIALIZERS / VIEWS PROFILE
# ---------------------------------------------------------------------
print("=" * 78)
print("15. SERIALIZERS / VIEWS PROFILS")
print("=" * 78)

for relative in [
    "nsikay_profiles/models.py",
    "nsikay_profiles/serializers.py",
    "nsikay_profiles/views.py",
    "nsikay_profiles/urls.py",
    "nsikay_activities/models.py",
    "nsikay_activities/serializers.py",
    "nsikay_activities/views.py",
    "api/serializers.py",
    "api/views.py",
    "api/urls.py",
    "core/models.py",
]:
    path = ROOT / "backend" / relative

    if not path.exists():
        print("ABSENT :", relative)
        continue

    print()
    print("-" * 78)
    print(relative)
    print("-" * 78)

    try:
        lines = path.read_text(encoding="utf-8").splitlines()

        interesting = (
            "class ",
            "profile_type",
            "is_primary",
            "create(",
            "update(",
            "delete(",
            "permission",
            "NsikayProfile",
            "Profile",
            "Activity",
            "urlpatterns",
            "path(",
            "router",
        )

        for lineno, line in enumerate(lines, 1):
            if any(token in line for token in interesting):
                print(f"{lineno:5}: {line}")

    except Exception as exc:
        print("READ ERROR :", repr(exc))

print()

# ---------------------------------------------------------------------
# 16. FRONTEND PROFILE ARCHITECTURE
# ---------------------------------------------------------------------
print("=" * 78)
print("16. FRONTEND - PROFILS / ACTIVITES / ENGAGEMENT")
print("=" * 78)

frontend = ROOT / "frontend" / "src"

if frontend.exists():
    for path in frontend.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in {".jsx", ".js", ".tsx", ".ts"}:
            continue

        if "node_modules" in {p.lower() for p in path.parts}:
            continue

        name = path.name.lower()

        if any(x in name for x in (
            "profile",
            "dashboard",
            "activity",
            "activit",
            "engagement",
            "app.",
        )):
            print(path.relative_to(ROOT))

print()

# ---------------------------------------------------------------------
# 17. FRONTEND PROFILE TYPE REFERENCES
# ---------------------------------------------------------------------
print("=" * 78)
print("17. FRONTEND - ANCIENS PROFILE_TYPES")
print("=" * 78)

if frontend.exists():
    for path in frontend.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in {".jsx", ".js", ".tsx", ".ts"}:
            continue

        if "node_modules" in {p.lower() for p in path.parts}:
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue

        hits = []

        for lineno, line in enumerate(lines, 1):
            if (
                "PROFILE_TYPES" in line
                or "profile_type" in line
                or '"/profils"' in line
                or "'/profils'" in line
            ):
                hits.append((lineno, line.strip()))

        if hits:
            print()
            print(path.relative_to(ROOT))
            for lineno, line in hits:
                print(f"  {lineno}: {line}")

print()

# ---------------------------------------------------------------------
# 18. FRONTEND ROUTES
# ---------------------------------------------------------------------
print("=" * 78)
print("18. FRONTEND - ROUTES")
print("=" * 78)

app_files = []

if frontend.exists():
    app_files = [
        p for p in frontend.rglob("*.jsx")
        if p.name.lower() == "app.jsx"
    ] + [
        p for p in frontend.rglob("*.js")
        if p.name.lower() == "app.js"
    ]

for path in app_files:
    print()
    print(path.relative_to(ROOT))

    try:
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            if (
                "Route" in line
                or "path=" in line
                or "navigate(" in line
            ):
                print(f"{lineno:5}: {line.strip()}")
    except Exception as exc:
        print("READ ERROR :", repr(exc))

print()

# ---------------------------------------------------------------------
# 19. MIGRATIONS PROFILE
# ---------------------------------------------------------------------
print("=" * 78)
print("19. MIGRATIONS PROFILS")
print("=" * 78)

for app_name in ["core", "nsikay_profiles", "nsikay_activities"]:
    migration_dir = ROOT / "backend" / app_name / "migrations"

    if not migration_dir.exists():
        print(f"{app_name}: aucune migration")
        continue

    print()
    print(app_name)

    for path in sorted(migration_dir.glob("*.py")):
        if path.name == "__init__.py":
            continue

        print(" ", path.name)

        try:
            text = path.read_text(encoding="utf-8")

            for keyword in [
                "profile_type",
                "is_primary",
                "NsikayProfile",
                "Profile",
                "Activity",
                "CreateModel",
                "DeleteModel",
                "AlterField",
            ]:
                if keyword in text:
                    print("    ->", keyword)
        except Exception:
            pass

print()

# ---------------------------------------------------------------------
# 20. MIGRATIONS DATABASE
# ---------------------------------------------------------------------
print("=" * 78)
print("20. ETAT DES MIGRATIONS EN BASE")
print("=" * 78)

try:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT app, name
            FROM django_migrations
            ORDER BY app, id
        """)

        current_app = None

        for app, name in cursor.fetchall():
            if app != current_app:
                current_app = app
                print()
                print(app)

            print("   ", name)

except Exception as exc:
    print("MIGRATION DB ERROR :", repr(exc))

print()

# ---------------------------------------------------------------------
# 21. USERS - INFORMATION MINIMALE
# ---------------------------------------------------------------------
print("=" * 78)
print("21. UTILISATEURS ACTUELS")
print("=" * 78)

try:
    from django.contrib.auth import get_user_model

    User = get_user_model()

    for user in User.objects.all().order_by("id"):
        print(
            f"id={user.id} "
            f"username={user.username!r} "
            f"active={user.is_active} "
            f"staff={user.is_staff} "
            f"superuser={user.is_superuser}"
        )

except Exception as exc:
    print("USER ERROR :", repr(exc))

print()

# ---------------------------------------------------------------------
# 22. PROFILE COUNTS
# ---------------------------------------------------------------------
print("=" * 78)
print("22. DONNEES EXISTANTES DES PROFILS")
print("=" * 78)

for model in profile_models:
    try:
        count = model.objects.count()
        print(
            f"{model._meta.app_label}.{model.__name__}"
            f" : {count} ligne(s)"
        )

        if hasattr(model, "PROFILE_TYPES"):
            try:
                rows = (
                    model.objects
                    .values("profile_type")
                    .annotate(total=__import__("django").db.models.Count("id"))
                    .order_by("profile_type")
                )

                for row in rows:
                    print(
                        f"    {row['profile_type']!r}"
                        f" -> {row['total']}"
                    )
            except Exception as exc:
                print("    profile_type stats ERROR :", repr(exc))

    except Exception as exc:
        print(
            f"{model._meta.app_label}.{model.__name__}"
            f" ERROR : {repr(exc)}"
        )

print()

# ---------------------------------------------------------------------
# 23. ACTIVE OBJECT CREATIONS - SELECTED FINANCIAL / BUSINESS AREAS
# ---------------------------------------------------------------------
print("=" * 78)
print("23. CREATIONS OBJECTS ACTIVES - ZONES SENSIBLES")
print("=" * 78)

active_roots = [
    ROOT / "backend" / "finance",
    ROOT / "backend" / "wallet",
    ROOT / "backend" / "banking",
    ROOT / "backend" / "wenze",
    ROOT / "backend" / "gift_resellers",
    ROOT / "backend" / "certification",
    ROOT / "backend" / "administration",
    ROOT / "backend" / "business",
    ROOT / "backend" / "financial_routing",
]

for base in active_roots:
    if not base.exists():
        continue

    for path in base.rglob("*.py"):
        if is_ignored(path):
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue

        hits = []

        for lineno, line in enumerate(lines, 1):
            if ".objects.create(" in line or ".objects.get_or_create(" in line:
                hits.append((lineno, line.strip()))

        if hits:
            print()
            print(path.relative_to(ROOT))
            for lineno, line in hits:
                print(f"  {lineno}: {line}")

print()

# ---------------------------------------------------------------------
# 24. SUMMARY
# ---------------------------------------------------------------------
print("=" * 78)
print("24. RESUME AUTOMATIQUE")
print("=" * 78)

print()
print("POINTS A VERIFIER EN PRIORITE :")

checks = []

if any(
    m.__name__ == "Profile"
    for m in apps.get_models()
):
    checks.append("core.Profile est encore enregistre par Django")

if any(
    m.__name__ == "NsikayProfile"
    for m in apps.get_models()
):
    checks.append("nsikay_profiles.NsikayProfile est encore actif")

if any(
    "profile_type" in [f.name for f in m._meta.fields]
    for m in apps.get_models()
):
    checks.append("au moins un modele actif contient encore profile_type")

if "events_eventregistration" not in db_tables:
    checks.append("events_eventregistration absente de PostgreSQL")

if "media_eventregistration" in db_tables:
    checks.append("media_eventregistration existe")

for item in checks:
    print(" -", item)

if not checks:
    print("Aucun point automatique detecte.")

print()
print("=" * 78)
print("FIN DE L'AUDIT")
print("AUCUNE MODIFICATION EFFECTUEE")
print("=" * 78)
