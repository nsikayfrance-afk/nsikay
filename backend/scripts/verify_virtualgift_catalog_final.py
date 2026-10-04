import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from api_nsikay.models import VirtualGift

expected = [
    ("Quartz", "0.10"),
    ("Calcite", "0.20"),
    ("Fluorite", "0.50"),
    ("Obsidienne", "1.00"),
    ("Améthyste", "2.00"),
    ("Grenat", "5.00"),
    ("Topaze", "10.00"),
    ("Aigue-marine", "20.00"),
    ("Émeraude", "50.00"),
    ("Saphir", "100.00"),
    ("Rubis", "200.00"),
    ("Or", "500.00"),
    ("Platine", "1000.00"),
    ("Palladium", "2500.00"),
    ("Diamant", "5000.00"),
    ("Diamant Noir", "10000.00"),
    ("Diamant Bleu", "25000.00"),
    ("Diamant Royal", "50000.00"),
    ("Diamant Impérial", "100000.00"),
]

print("")
print("=" * 70)
print(" NSIKAY - VERIFICATION CATALOGUE VIRTUALGIFT")
print("=" * 70)

gifts = list(
    VirtualGift.objects
    .order_by("display_order", "value_eur", "id")
)

print("")
print("TOTAL EN BASE :", len(gifts))
print("TOTAL ATTENDU :", len(expected))

print("")
print("===== CATALOGUE =====")

for gift in gifts:
    print(
        f"{gift.display_order:02d} | "
        f"{gift.name:20s} | "
        f"{gift.value_eur:>12} EUR | "
        f"{gift.currency} | "
        f"{gift.currency_reference} | "
        f"{gift.category} | "
        f"active={gift.active} | "
        f"avatar={'OUI' if gift.avatar else 'NON'}"
    )

print("")
print("===== CONTROLES =====")

errors = []

if len(gifts) != len(expected):
    errors.append(
        f"Nombre incorrect : {len(gifts)} au lieu de {len(expected)}"
    )

for index, (expected_name, expected_value) in enumerate(expected, start=1):

    matches = [
        g for g in gifts
        if g.name == expected_name
        and str(g.value_eur) == expected_value
    ]

    if not matches:
        errors.append(
            f"Manquant ou incorrect : {expected_name} / {expected_value} EUR"
        )

for gift in gifts:

    if gift.currency != "EUR":
        errors.append(f"{gift.name}: currency != EUR")

    if gift.currency_reference != "EUR":
        errors.append(f"{gift.name}: currency_reference != EUR")

    if gift.category != "MINERAL":
        errors.append(f"{gift.name}: category != MINERAL")

    if not gift.active:
        errors.append(f"{gift.name}: cadeau inactif")

    if not gift.avatar:
        errors.append(f"{gift.name}: avatar absent")

    metadata = gift.metadata or {}

    if metadata.get("stock_management") is not False:
        errors.append(f"{gift.name}: stock_management incorrect")

    if metadata.get("stock_depletion") is not False:
        errors.append(f"{gift.name}: stock_depletion incorrect")

print("Erreurs :", len(errors))

if errors:
    for error in errors:
        print("ERREUR :", error)

    print("")
    print("RESULTAT : CATALOGUE A CORRIGER")
else:
    print("")
    print("RESULTAT : CATALOGUE 19/19 VALIDE")
    print("Catalogue permanent : OUI")
    print("Gestion de stock     : NON")
    print("Devise de référence  : EUR")
    print("Devises d'affichage  : EUR / USD / CDF")

print("")
print("=" * 70)