import os
from decimal import Decimal
from pathlib import Path
from django.core.files import File
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from api_nsikay.models import VirtualGift


ROOT = Path(__file__).resolve().parents[2]
AVATAR_DIR = ROOT / "backend" / "media" / "gift_avatars"

GIFTS = [
    ("Quartz", "quartz", "0.10"),
    ("Calcite", "calcite", "0.20"),
    ("Fluorite", "fluorite", "0.50"),
    ("Obsidienne", "obsidienne", "1.00"),
    ("Améthyste", "amethyste", "2.00"),
    ("Grenat", "grenat", "5.00"),
    ("Topaze", "topaze", "10.00"),
    ("Aigue-marine", "aigue-marine", "20.00"),
    ("Émeraude", "emeraude", "50.00"),
    ("Saphir", "saphir", "100.00"),
    ("Rubis", "rubis", "200.00"),
    ("Or", "or", "500.00"),
    ("Platine", "platine", "1000.00"),
    ("Palladium", "palladium", "2500.00"),
    ("Diamant", "diamant", "5000.00"),
    ("Diamant Noir", "diamant-noir", "10000.00"),
    ("Diamant Bleu", "diamant-bleu", "25000.00"),
    ("Diamant Royal", "diamant-royal", "50000.00"),
    ("Diamant Impérial", "diamant-imperial", "100000.00"),
]


def make_avatar(name, value, path):

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="512" height="512" viewBox="0 0 512 512">
<rect width="512" height="512" rx="90" fill="#102a43"/>
<polygon
points="256,60 410,175 350,365 256,445 162,365 102,175"
fill="#dbeafe"
stroke="#ffffff"
stroke-width="8"/>
<polygon
points="256,60 410,175 256,445"
fill="#ffffff"
opacity="0.30"/>
<polygon
points="256,60 256,445 102,175"
fill="#94a3b8"
opacity="0.35"/>
<text x="256" y="472"
text-anchor="middle"
font-family="Arial"
font-size="25"
font-weight="bold"
fill="white">{name}</text>
<text x="256" y="500"
text-anchor="middle"
font-family="Arial"
font-size="17"
fill="#dbeafe">{value} EUR</text>
</svg>'''

    path.write_text(svg, encoding="utf-8")
    return path


@transaction.atomic
def main():

    AVATAR_DIR.mkdir(parents=True, exist_ok=True)

    before = VirtualGift.objects.count()

    print("")
    print("=" * 70)
    print(" NSIKAY - CREATION STRICTE CATALOGUE VIRTUALGIFT")
    print("=" * 70)
    print("")
    print("Avant :", before)

    if before != 0:
        raise RuntimeError(
            f"Le catalogue contient déjà {before} cadeaux. "
            "Arrêt volontaire pour éviter une insertion incorrecte."
        )

    created = []

    for position, (name, slug, value_text) in enumerate(GIFTS, start=1):

        value = Decimal(value_text)

        avatar_filename = f"{slug}.svg"
        avatar_path = AVATAR_DIR / avatar_filename

        make_avatar(
            name,
            value_text,
            avatar_path
        )

        gift = VirtualGift.objects.create(
            name=name,
            slug=slug,
            value=value,
            currency="EUR",
            value_eur=value,
            currency_reference="EUR",
            category="MINERAL",
            active=True,
            display_order=position,
            metadata={
                "catalogue": "NSIKAY",
                "catalogue_type": "PERMANENT_GIFT",
                "reference_currency": "EUR",
                "stock_management": False,
                "stock_depletion": False,
                "display_currencies": ["EUR", "USD", "CDF"],
            },
        )

        with avatar_path.open("rb") as f:
            gift.avatar.save(
                avatar_filename,
                File(f),
                save=True
            )

        created.append(gift)

        print(
            f"OK {position:02d}/19 | "
            f"{name:20s} | "
            f"{value} EUR | "
            f"avatar=OK"
        )

    final_count = VirtualGift.objects.count()

    print("")
    print("Avant :", before)
    print("Créés :", len(created))
    print("Après :", final_count)

    if final_count != 19:
        raise RuntimeError(
            f"ECHEC : {final_count} cadeaux présents au lieu de 19."
        )

    print("")
    print("===== VERIFICATION =====")

    for gift in VirtualGift.objects.order_by("display_order"):
        print(
            f"{gift.display_order:02d} | "
            f"{gift.name:20s} | "
            f"{gift.value_eur} EUR | "
            f"{gift.currency} | "
            f"{gift.category} | "
            f"active={gift.active} | "
            f"avatar={'OK' if gift.avatar else 'ABSENT'}"
        )

    print("")
    print("RESULTAT : CATALOGUE 19/19 CREE AVEC SUCCES")


main()