from pathlib import Path
import re

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\api_nsikay\models.py")

text = path.read_text(encoding="utf-8")

print("")
print("=" * 70)
print("PATCH MODELE GIFTTRANSACTION")
print("=" * 70)

# ------------------------------------------------------------------
# Vérification
# ------------------------------------------------------------------

if "class GiftTransaction(models.Model):" not in text:
    raise RuntimeError(
        "La classe GiftTransaction est introuvable."
    )

# ------------------------------------------------------------------
# Ne pas appliquer deux fois
# ------------------------------------------------------------------

if "publication = models.ForeignKey(" in text and \
   "class GiftTransaction(models.Model):" in text:

    print("Le modèle GiftTransaction semble déjà intégrer la publication.")
    print("Aucune modification supplémentaire du modèle.")

else:

    pattern = re.compile(
        r"class GiftTransaction\(models\.Model\):"
        r"(?P<body>.*?)(?=\nclass |\Z)",
        re.S
    )

    match = pattern.search(text)

    if not match:
        raise RuntimeError(
            "Bloc GiftTransaction introuvable."
        )

    block = match.group(0)

    if "created_at = models.DateTimeField" not in block:
        raise RuntimeError(
            "Le champ created_at de GiftTransaction est introuvable."
        )

    addition = '''

    publication = models.ForeignKey(
        "api_nsikay.SocialPost",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gift_transactions",
    )

    live = models.ForeignKey(
        "tv_regie.LiveStream",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gift_transactions",
    )

    amount_eur = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
    )

    payment_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
    )

    payment_currency = models.CharField(
        max_length=3,
        default="EUR",
    )

    status = models.CharField(
        max_length=30,
        default="PENDING",
    )

    reference = models.CharField(
        max_length=120,
        unique=True,
        null=True,
        blank=True,
    )

    payment_reference = models.CharField(
        max_length=120,
        null=True,
        blank=True,
    )

    financial_ledger_reference = models.CharField(
        max_length=120,
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )
'''

    marker = re.search(
        r"(\n\s*created_at\s*=\s*models\.DateTimeField\([^\n]*\))",
        block
    )

    if not marker:
        raise RuntimeError(
            "Impossible de localiser created_at."
        )

    insertion_point = marker.end()

    new_block = (
        block[:insertion_point]
        + addition
        + block[insertion_point:]
    )

    text = (
        text[:match.start()]
        + new_block
        + text[match.end():]
    )

    path.write_text(
        text,
        encoding="utf-8"
    )

    print("GiftTransaction modifié avec succès.")

print("")
print("Champs attendus :")

for field in [
    "publication",
    "live",
    "amount_eur",
    "payment_amount",
    "payment_currency",
    "status",
    "reference",
    "payment_reference",
    "financial_ledger_reference",
    "metadata",
]:

    if field in text:
        print("OK :", field)
    else:
        print("ERREUR :", field)

print("")
print("PATCH TERMINE")