import os
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.apps import apps

lines = []

def section(title):
    lines.append("")
    lines.append("=" * 72)
    lines.append(title)
    lines.append("=" * 72)

section("NSIKAY - PREPARATION AVATARS CADEAUX 10")
lines.append("LECTURE SEULE - AUCUNE MODIFICATION DE BASE")

# ------------------------------------------------------------
# MODELE CADEAU EXISTANT
# ------------------------------------------------------------
section("MODELE VIRTUAL GIFT")

try:
    VirtualGift = apps.get_model("api_nsikay", "VirtualGift")

    lines.append(f"TABLE : {VirtualGift._meta.db_table}")
    lines.append(f"TOTAL : {VirtualGift.objects.count()}")

    for field in VirtualGift._meta.fields:
        lines.append(
            f"FIELD={field.name} | "
            f"TYPE={field.__class__.__name__} | "
            f"NULL={field.null} | "
            f"BLANK={field.blank} | "
            f"DEFAULT={field.default}"
        )
except Exception as e:
    lines.append(f"ERREUR VirtualGift : {e}")

# ------------------------------------------------------------
# TRANSACTION CADEAU
# ------------------------------------------------------------
section("MODELE GIFT TRANSACTION")

try:
    GiftTransaction = apps.get_model(
        "api_nsikay",
        "GiftTransaction"
    )

    lines.append(f"TABLE : {GiftTransaction._meta.db_table}")
    lines.append(f"TOTAL : {GiftTransaction.objects.count()}")

    for field in GiftTransaction._meta.fields:
        lines.append(
            f"FIELD={field.name} | "
            f"TYPE={field.__class__.__name__} | "
            f"NULL={field.null} | "
            f"BLANK={field.blank}"
        )
except Exception as e:
    lines.append(f"ERREUR GiftTransaction : {e}")

# ------------------------------------------------------------
# PUBLICATION
# ------------------------------------------------------------
section("MODELE SOCIAL POST")

try:
    SocialPost = apps.get_model(
        "api_nsikay",
        "SocialPost"
    )

    lines.append(f"TABLE : {SocialPost._meta.db_table}")
    lines.append(f"TOTAL : {SocialPost.objects.count()}")

    for field in SocialPost._meta.fields:
        lines.append(
            f"FIELD={field.name} | "
            f"TYPE={field.__class__.__name__}"
        )
except Exception as e:
    lines.append(f"ERREUR SocialPost : {e}")

# ------------------------------------------------------------
# CREATEUR
# ------------------------------------------------------------
section("MODELE CREATOR PROFILE")

try:
    CreatorProfile = apps.get_model(
        "api_nsikay",
        "CreatorProfile"
    )

    lines.append(f"TABLE : {CreatorProfile._meta.db_table}")
    lines.append(f"TOTAL : {CreatorProfile.objects.count()}")

    for field in CreatorProfile._meta.fields:
        lines.append(
            f"FIELD={field.name} | "
            f"TYPE={field.__class__.__name__}"
        )
except Exception as e:
    lines.append(f"ERREUR CreatorProfile : {e}")

# ------------------------------------------------------------
# MEDIA CONFIGURATION
# ------------------------------------------------------------
section("CONFIGURATION MEDIA")

from django.conf import settings

lines.append(f"MEDIA_ROOT={getattr(settings, 'MEDIA_ROOT', None)}")
lines.append(f"MEDIA_URL={getattr(settings, 'MEDIA_URL', None)}")
lines.append(
    f"DEFAULT_FILE_STORAGE="
    f"{getattr(settings, 'DEFAULT_FILE_STORAGE', None)}"
)

# ------------------------------------------------------------
# DOSSIERS
# ------------------------------------------------------------
section("DOSSIERS AVATARS PROPOSES")

avatar_root = Path(
    r"C:\Users\DELL Technologies\Desktop\nsikay nante"
    r"\backend\media\gift_avatars"
)

lines.append(f"ROOT={avatar_root}")
lines.append(f"EXISTE={avatar_root.exists()}")

for name in [
    "quartz",
    "calcite",
    "fluorite",
    "obsidienne",
    "amethyste",
    "grenat",
    "topaze",
    "aigue_marine",
    "emeraude",
    "saphir",
    "rubis",
    "or",
    "platine",
    "palladium",
    "diamant",
    "diamant_noir",
    "diamant_bleu",
    "diamant_royal",
    "diamant_imperial",
    "cristal_rare",
]:
    lines.append(
        f"AVATAR={name} | "
        f"FICHIER={avatar_root / (name + '.png')}"
    )

# ------------------------------------------------------------
# DESIGN CIBLE
# ------------------------------------------------------------
section("STRUCTURE CIBLE")

lines.extend([
    "VirtualGift",
    "  - name",
    "  - slug",
    "  - value_eur",
    "  - currency_reference",
    "  - avatar",
    "  - category",
    "  - active",
    "  - display_order",
    "  - metadata",
    "",
    "PRINCIPE :",
    "  valeur catalogue = EUR",
    "  affichage = devise principale utilisateur",
    "  avatar = fichier image du cadeau",
    "  aucun stock",
    "  catalogue permanent",
    "",
    "DEVISES PRINCIPALES : EUR / USD / CDF",
])

# ------------------------------------------------------------
# FIN
# ------------------------------------------------------------
section("FIN")

out = Path(
    r"C:\Users\DELL Technologies\Desktop\nsikay nante"
    r"\reports\gifts\PREPARATION_AVATARS_CADEAUX_10.txt"
)

out.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print("=" * 72)
print("PREPARATION AVATARS CADEAUX 10 TERMINEE")
print("=" * 72)
print("AUCUNE MODIFICATION DE BASE")
print(f"Rapport : {out}")