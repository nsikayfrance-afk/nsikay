from pathlib import Path

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\scripts\test_gift_resellers_stage4c.py")
lines = path.read_text(encoding="utf-8").splitlines()

start = None
end = None

for i, line in enumerate(lines):
    if "TEST 3 - DOUBLE ALLOCATION" in line:
        start = max(0, i - 5)
    if start is not None and "TEST 5" in line:
        end = min(len(lines), i + 5)
        break

if start is None:
    raise SystemExit("TEST_3_NOT_FOUND")

if end is None:
    end = min(len(lines), start + 180)

print("=" * 70)
print(" STAGE 4C - TESTS 3 ET 4")
print("=" * 70)

for n in range(start, end):
    print(f"{n+1:4} | {lines[n]}")