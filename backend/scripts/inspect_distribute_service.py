from pathlib import Path

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\gift_resellers\services.py")
lines = path.read_text(encoding="utf-8").splitlines()

print("")
print("============================================================")
print(" INSPECTION DISTRIBUTE_GIFT_UNIT")
print("============================================================")
print("")

for number, line in enumerate(lines, start=1):
    if "def distribute_gift_unit" in line:
        start = max(1, number - 5)
        end = min(len(lines), number + 75)

        for n in range(start, end + 1):
            print(f"{n:4}: {lines[n-1]}")

        break
else:
    print("FONCTION distribute_gift_unit INTROUVABLE")

print("")
print("============================================================")
print(" FIN INSPECTION")
print("============================================================")