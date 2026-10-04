from pathlib import Path
import re

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\api_nsikay\models.py")

text = path.read_text(encoding="utf-8")

print("")
print("=" * 80)
print(" NSIKAY - PATCH GIFTTRANSACTION V2")
print("=" * 80)

start_marker = "class GiftTransaction(models.Model):"

if start_marker not in text:
    raise RuntimeError("Classe GiftTransaction introuvable.")

start = text.index(start_marker)

next_match = re.search(
    r"\nclass\s+\w+\(models\.Model\):",
    text[start + len(start_marker):]
)

if next_match:
    end = start + len(start_marker) + next_match.start()
else:
    end = len(text)

block = text[start:end]

print("")
print("===== BLOC ACTUEL =====")
print(block)
print("===== FIN BLOC ACTUEL =====")

required = [
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
]

existing = []

for field in required:
    if re.search(
        rf"^\s*{re.escape(field)}\s*=",
        block,
        re.MULTILINE
    ):
        existing.append(field)

if len(existing) == len(required):
    print("")
    print("GiftTransaction est déjà intégré.")
    print("Aucune modification.")
else:

    if existing:
        print("")
        print("Champs déjà présents :")
        for field in existing:
            print("  -", field)

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

    # On insère juste avant la fin du bloc GiftTransaction.
    # Cela évite toute dépendance à la forme exacte de created_at.
    insertion = block.rstrip() + addition + "\n"

    new_text = (
        text[:start]
        + insertion
        + text[end:]
    )

    path.write_text(
        new_text,
        encoding="utf-8"
    )

    print("")
    print("PATCH APPLIQUE.")

print("")
print("=" * 80)
print(" VERIFICATION DU FICHIER")
print("=" * 80)

text2 = path.read_text(encoding="utf-8")

start2 = text2.index(start_marker)

next_match2 = re.search(
    r"\nclass\s+\w+\(models\.Model\):",
    text2[start2 + len(start_marker):]
)

if next_match2:
    end2 = start2 + len(start_marker) + next_match2.start()
else:
    end2 = len(text2)

block2 = text2[start2:end2]

ok = True

for field in required:

    if re.search(
        rf"^\s*{re.escape(field)}\s*=",
        block2,
        re.MULTILINE
    ):
        print("OK   ", field)
    else:
        print("FAIL ", field)
        ok = False

if not ok:
    raise RuntimeError(
        "Un ou plusieurs champs GiftTransaction sont absents."
    )

print("")
print("RESULTAT : PATCH GIFTTRANSACTION V2 = OK")