from pathlib import Path

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\gift_resellers\models.py")
lines = path.read_text(encoding="utf-8").splitlines()

print("")
print("=" * 70)
print(" INSPECTION EXACTE DistributionAgreement")
print("=" * 70)
print("")

start = None

for number, line in enumerate(lines, start=1):
    if line.strip().startswith("class DistributionAgreement"):
        start = number
        break

if start is None:
    print("CLASSE DistributionAgreement INTROUVABLE")
else:
    end = len(lines)

    # On s'arrête à la prochaine classe de même niveau.
    for number in range(start + 1, len(lines) + 1):
        line = lines[number - 1]

        if (
            line.startswith("class ")
            and not line.startswith("class DistributionAgreement")
        ):
            end = number - 1
            break

    print(f"DEBUT CLASSE : ligne {start}")
    print(f"FIN CLASSE   : ligne {end}")
    print("")

    for number in range(start, end + 1):
        print(f"{number:4}: {lines[number - 1]}")

print("")
print("=" * 70)
print(" RECHERCHE DES MECANISMES DE VERROUILLAGE")
print("=" * 70)
print("")

patterns = [
    "def save",
    "def clean",
    "LOCKED",
    "locked_at",
    "ValidationError",
    "previous_agreement",
]

for number, line in enumerate(lines, start=1):
    if any(pattern in line for pattern in patterns):
        print(f"{number:4}: {line}")

print("")
print("=" * 70)
print(" FIN INSPECTION")
print("=" * 70)