from pathlib import Path
import ast

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\gift_resellers\models.py")
source = path.read_text(encoding="utf-8")
tree = ast.parse(source)
lines = source.splitlines()

found = False

for node in tree.body:
    if isinstance(node, ast.ClassDef) and node.name == "SaleAllocation":
        found = True

        print("=" * 70)
        print(" MODELE SaleAllocation")
        print("=" * 70)
        print(f"LIGNES : {node.lineno} -> {node.end_lineno}")
        print()

        for number in range(node.lineno, node.end_lineno + 1):
            print(f"{number:4} | {lines[number - 1]}")

        print()
        print("MODELE=OK")
        break

if not found:
    raise SystemExit("SALE_ALLOCATION_NOT_FOUND")