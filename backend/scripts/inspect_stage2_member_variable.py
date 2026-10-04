from pathlib import Path

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\scripts\test_gift_resellers_stage2_final.py")
lines = path.read_text(encoding="utf-8").splitlines()

print("")
print("============================================================")
print(" INSPECTION VARIABLE MEMBER - STAGE 2")
print("============================================================")
print("")

for number, line in enumerate(lines, start=1):
    if (
        "member =" in line
        or "member=" in line
        or "member.id" in line
        or "current_member" in line
        or "NetworkMember.objects" in line
    ):
        print(f"{number:4}: {line}")

print("")
print("============================================================")
print(" BLOC AUTOUR DE LA CREATION DU NETWORK MEMBER")
print("============================================================")
print("")

for number, line in enumerate(lines, start=1):
    if "NetworkMember.objects" in line:
        start = max(1, number - 8)
        end = min(len(lines), number + 15)

        for n in range(start, end + 1):
            print(f"{n:4}: {lines[n-1]}")

        print("")

print("============================================================")
print(" FIN INSPECTION")
print("============================================================")