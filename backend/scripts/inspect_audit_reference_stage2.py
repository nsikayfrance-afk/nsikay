from pathlib import Path
import re

service = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\gift_resellers\services.py")
test = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\scripts\test_gift_resellers_stage2_final.py")

service_text = service.read_text(encoding="utf-8")
test_text = test.read_text(encoding="utf-8")

print("=" * 70)
print("SERVICES.PY - AUDIT")
print("=" * 70)

lines = service_text.splitlines()

for i, line in enumerate(lines, 1):
    if "GiftResellerAuditLog" in line or "reference=" in line:
        start = max(1, i - 3)
        end = min(len(lines), i + 3)

        print("")
        print(f"--- autour de la ligne {i} ---")

        for n in range(start, end + 1):
            print(f"{n:4}: {lines[n-1]}")

print("")
print("=" * 70)
print("TEST - AUDIT UNITÉ")
print("=" * 70)

test_lines = test_text.splitlines()

for i, line in enumerate(test_lines, 1):
    if "AUDIT UNIT" in line or "audit" in line.lower() and "filter" in line:
        start = max(1, i - 5)
        end = min(len(test_lines), i + 8)

        print("")
        print(f"--- autour de la ligne {i} ---")

        for n in range(start, end + 1):
            print(f"{n:4}: {test_lines[n-1]}")

print("")
print("=" * 70)
print("OCCURRENCES REFERENCE / UNIT_ID")
print("=" * 70)

for i, line in enumerate(test_lines, 1):
    if "reference" in line.lower() or "unit_id" in line.lower():
        print(f"{i:4}: {line}")

print("")
print("=" * 70)
print("FIN INSPECTION")
print("=" * 70)