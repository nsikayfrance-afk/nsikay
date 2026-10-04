import os
import django
from pathlib import Path
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from django.apps import apps
from django.contrib.auth.models import User, Group
from django.db import connection
from django.db.models import Q

OUT = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\reports\gifts\AUDIT_CADEAUX_FINAL_07.txt")

lines = []

def section(title):
    lines.append("")
    lines.append("=" * 70)
    lines.append(title)
    lines.append("=" * 70)

def model_info(model):
    lines.append(f"MODEL : {model._meta.label}")
    lines.append(f"TABLE : {model._meta.db_table}")
    for f in model._meta.fields:
        remote = ""
        if getattr(f, "remote_field", None) is not None:
            remote_model = getattr(f.remote_field, "model", None)
            if remote_model:
                remote = f" -> {remote_model._meta.label}"
        lines.append(
            f"  {f.name} | {f.__class__.__name__} | "
            f"null={getattr(f,'null',None)} | blank={getattr(f,'blank',None)}{remote}"
        )
    if model._meta.constraints:
        lines.append("CONTRAINTES :")
        for c in model._meta.constraints:
            lines.append(f"  {c}")
    if model._meta.unique_together:
        lines.append(f"UNIQUE_TOGETHER : {model._meta.unique_together}")
    lines.append("")

section("NSIKAY - AUDIT CADEAUX FINAL 07")
lines.append("MODE : LECTURE SEULE - AUCUNE MODIFICATION")
lines.append(f"BASE : {connection.settings_dict.get('NAME')}")
lines.append(f"ENGINE : {connection.settings_dict.get('ENGINE')}")

# ------------------------------------------------------------
# MODELES FINANCIAL ACCOUNTS
# ------------------------------------------------------------
section("FINANCIAL_ACCOUNTS")

for label in [
    "financial_accounts.GiftFinancialLedger",
]:
    try:
        model = apps.get_model(label)
        model_info(model)
        try:
            lines.append(f"COUNT : {model.objects.count()}")
        except Exception as e:
            lines.append(f"COUNT ERROR : {e}")
    except Exception as e:
        lines.append(f"MODELE ABSENT : {label} -> {e}")

# ------------------------------------------------------------
# MODELES WALLET OPERATIONNELS
# ------------------------------------------------------------
section("WALLET OPERATIONNEL")

for label in [
    "wallet.Wallet",
    "wallet.WalletBalance",
    "wallet.WalletTransaction",
    "wallet.WalletOperation",
    "wallet.WalletCommission",
    "wallet.WalletAuditLog",
    "wallet.WalletCurrencyBalance",
    "wallet.WalletKYCProfile",
    "wallet.WalletBankAccount",
]:
    try:
        model = apps.get_model(label)
        model_info(model)
        try:
            lines.append(f"COUNT : {model.objects.count()}")
        except Exception as e:
            lines.append(f"COUNT ERROR : {e}")
    except Exception as e:
        lines.append(f"MODELE ABSENT : {label} -> {e}")

# ------------------------------------------------------------
# MODELES CADEAUX / CREATEURS / PUBLICATIONS
# ------------------------------------------------------------
section("CADEAUX - CREATEURS - PUBLICATIONS")

for label in [
    "api_nsikay.VirtualGift",
    "api_nsikay.GiftTransaction",
    "api_nsikay.CreatorProfile",
    "api_nsikay.SocialPost",
]:
    try:
        model = apps.get_model(label)
        model_info(model)
        try:
            lines.append(f"COUNT : {model.objects.count()}")
        except Exception as e:
            lines.append(f"COUNT ERROR : {e}")
    except Exception as e:
        lines.append(f"MODELE ABSENT : {label} -> {e}")

# ------------------------------------------------------------
# MODELES LIVE / FAVORI EVENTUELS
# ------------------------------------------------------------
section("RECHERCHE LIVE / FAVORI / REWARD")

keywords = [
    "live", "livestream", "broadcast", "favori",
    "favorite", "creatorreward", "reward",
    "gift", "cadeau", "publicationreward"
]

for model in apps.get_models():
    label = model._meta.label.lower()
    name = model.__name__.lower()

    if any(k in label or k in name for k in keywords):
        lines.append(
            f"{model._meta.label} | table={model._meta.db_table}"
        )

# ------------------------------------------------------------
# GROUPES / PERMISSIONS
# ------------------------------------------------------------
section("GROUPES DJANGO")

for g in Group.objects.all().order_by("name"):
    lines.append(f"{g.name} | permissions={g.permissions.count()}")

# ------------------------------------------------------------
# USERROLE
# ------------------------------------------------------------
section("ROLES API NSIKAY")

try:
    UserRole = apps.get_model("api_nsikay", "UserRole")
    model_info(UserRole)

    for value, label in getattr(UserRole, "ROLE_CHOICES", []):
        lines.append(f"ROLE : {value} -> {label}")

except Exception as e:
    lines.append(f"UserRole absent : {e}")

# ------------------------------------------------------------
# SERVICES FINANCE
# ------------------------------------------------------------
section("SERVICES FINANCE WALLET")

service_files = [
    Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\finance\wallet_service.py"),
    Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\finance\fees.py"),
    Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\financial_accounts"),
]

for p in service_files:
    lines.append(f"PATH : {p}")
    if p.is_file():
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
            lines.append(text[:30000])
        except Exception as e:
            lines.append(f"READ ERROR : {e}")
    elif p.is_dir():
        for child in sorted(p.glob("*.py")):
            lines.append(f"--- FILE {child.name} ---")
            try:
                lines.append(
                    child.read_text(
                        encoding="utf-8",
                        errors="replace"
                    )[:30000]
                )
            except Exception as e:
                lines.append(f"READ ERROR : {e}")
    else:
        lines.append("ABSENT")

# ------------------------------------------------------------
# MIGRATIONS FINANCIAL ACCOUNTS
# ------------------------------------------------------------
section("MIGRATIONS FINANCIAL_ACCOUNTS")

migdir = Path(
    r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend"
) / "financial_accounts" / "migrations"

if migdir.exists():
    for p in sorted(migdir.glob("*.py")):
        lines.append(p.name)
else:
    lines.append("DOSSIER MIGRATIONS ABSENT")

# ------------------------------------------------------------
# REFERENCES GIFT FINANCIAL LEDGER
# ------------------------------------------------------------
section("REFERENCES GIFT FINANCIAL LEDGER")

root = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend")

for p in root.rglob("*.py"):
    try:
        if any(part == "backups" for part in p.parts):
            continue

        txt = p.read_text(encoding="utf-8", errors="replace")

        if "GiftFinancialLedger" in txt:
            lines.append(f"{p} :")
            for i, line in enumerate(txt.splitlines(), 1):
                if "GiftFinancialLedger" in line:
                    lines.append(f"  {i} | {line.strip()}")
    except Exception:
        pass

# ------------------------------------------------------------
# DJANGO CHECK
# ------------------------------------------------------------
section("FIN")

OUT.write_text("\n".join(lines), encoding="utf-8")

print("============================================================")
print(" AUDIT CADEAUX FINAL 07 TERMINE")
print("============================================================")
print(f"Rapport : {OUT}")
print("AUCUNE MODIFICATION EFFECTUEE")
print("============================================================")