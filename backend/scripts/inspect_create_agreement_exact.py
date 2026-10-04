from pathlib import Path

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\gift_resellers\services.py")
lines = path.read_text(encoding="utf-8").splitlines()

print("")
print("=" * 60)
print(" INSPECTION EXACTE create_distribution_agreement")
print("=" * 60)
print("")

start = None

for number, line in enumerate(lines, start=1):
    if "def create_distribution_agreement" in line:
        start = number
        break

if start is None:
    print("FONCTION INTROUVABLE")
else:
    end = min(len(lines), start + 130)

    for number in range(start, end + 1):
        print(f"{number:4}: {lines[number - 1]}")

print("")
print("=" * 60)
print(" RECHERCHE EFFECTIVE_FROM")
print("=" * 60)
print("")

for number, line in enumerate(lines, start=1):
    if "effective_from" in line:
        print(f"{number:4}: {line}")

print("")
print("=" * 60)
print(" FIN INSPECTION")
print("=" * 60)