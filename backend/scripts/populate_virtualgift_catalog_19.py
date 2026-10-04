import os
from decimal import Decimal
from pathlib import Path
from xml.sax.saxutils import escape

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.core.files import File
from django.db import transaction

from api_nsikay.models import VirtualGift


ROOT = Path(__file__).resolve().parents[2]
MEDIA_DIR = ROOT / "backend" / "media" / "gift_avatars"


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


def create_svg(name, value, filename):
    """
    Avatar SVG provisoire propre et léger.
    Il pourra être remplacé ultérieurement par une illustration
    graphique dédiée sans modifier le catalogue financier.
    """

    title = escape(name)
    value_text = escape(f"{value} EUR")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="512" height="512" viewBox="0 0 512 512">

<defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#0b1f3a"/>
        <stop offset="100%" stop-color="#183b66"/>
    </linearGradient>

    <linearGradient id="gem" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#ffffff"/>
        <stop offset="45%" stop-color="#d9e6f2"/>
        <stop offset="100%" stop-color="#8aa4bd"/>
    </linearGradient>
</defs>

<rect width="512" height="512" rx="96" fill="url(#bg)"/>

<polygon
    points="256,72 392,174 350,358 256,430 162,358 120,174"
    fill="url(#gem)"
    stroke="#ffffff"
    stroke-width="8"/>

<polygon
    points="256,72 256,430 162,358 120,174"
    fill="#b7c9d9"
    opacity="0.42"/>

<polygon
    points="256,72 392,174 256,430"
    fill="#ffffff"
    opacity="0.24"/>

<text
    x="256"
    y="465"
    text-anchor="middle"
    font-family="Arial, sans-serif"
    font-size="27"
    font-weight="700"
    fill="#ffffff">{title}</text>

<text
    x="256"
    y="495"
    text-anchor="middle"
    font-family="Arial, sans-serif"
    font-size="18"
    fill="#d9e6f2">{value_text}</text>

</svg>'''

    path = MEDIA_DIR / filename
    path.write_text(svg, encoding="utf-8")
    return path


@transaction.atomic
def populate():

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    print("")
    print("=" * 70)
    print(" NSIKAY - CATALOGUE PERMANENT DES 19 CADEAUX MINERAUX")
    print("=" * 70)

    print("")
    print("Catalogue attendu :", len(GIFTS))
    print("Catalogue existant :", VirtualGift.objects.count())

    created = 0
    updated = 0

    for index, (name, slug, value_text) in enumerate(GIFTS, start=1):

        value = Decimal(value_text)

        avatar_filename = f"{slug}.svg"
        avatar_path = create_svg(
            name=name,
            value=value_text,
            filename=avatar_filename,
        )

        obj, was_created = VirtualGift.objects.get_or_create(
            slug=slug,
            defaults={
                "name": name,
                "value": value,
                "currency": "EUR",
                "value_eur": value,
                "currency_reference": "EUR",
                "category": "MINERAL",
                "active": True,
                "display_order": index,
                "metadata": {
                    "catalogue": "NSIKAY",
                    "catalogue_type": "PERMANENT_GIFT",
                    "category": "MINERAL",
                    "reference_currency": "EUR",
                    "stock_management": False,
                    "stock_depletion": False,
                    "display_value_conversion": [
                        "EUR",
                        "USD",
                        "CDF",
                    ],
                },
            },
        )

        if was_created:
            created += 1
        else:
            updated += 1

            obj.name = name
            obj.value = value
            obj.currency = "EUR"
            obj.value_eur = value
            obj.currency_reference = "EUR"
            obj.category = "MINERAL"
            obj.active = True
            obj.display_order = index
            obj.metadata = {
                "catalogue": "NSIKAY",
                "catalogue_type": "PERMANENT_GIFT",
                "category": "MINERAL",
                "reference_currency": "EUR",
                "stock_management": False,
                "stock_depletion": False,
                "display_value_conversion": [
                    "EUR",
                    "USD",
                    "CDF",
                ],
            }

            obj.save()

        # Remplacement contrôlé de l'avatar.
        with avatar_path.open("rb") as avatar_file:
            obj.avatar.save(
                avatar_filename,
                File(avatar_file),
                save=True,
            )

        print(
            f"{index:02d}. "
            f"{name:20s} | "
            f"{value:>12} EUR | "
            f"{slug}"
        )

    print("")
    print("Créés :", created)
    print("Mis à jour :", updated)
    print("Total final :", VirtualGift.objects.count())

    if VirtualGift.objects.count() != len(GIFTS):
        raise RuntimeError(
            "Le nombre final de cadeaux ne correspond pas au catalogue attendu."
        )

    print("")
    print("===== CONTROLE FINAL =====")

    for gift in VirtualGift.objects.order_by("display_order"):
        print(
            f"{gift.display_order:02d} | "
            f"{gift.name:20s} | "
            f"{gift.value_eur:>12} EUR | "
            f"{gift.currency} | "
            f"{gift.category} | "
            f"active={gift.active} | "
            f"avatar={bool(gift.avatar)}"
        )

    print("")
    print("RESULTAT : CATALOGUE 19/19 VALIDE")


if __name__ == "__main__":
    populate()