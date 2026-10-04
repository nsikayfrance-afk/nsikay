from pathlib import Path
import ast

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\gift_resellers\services.py")
source = path.read_text(encoding="utf-8")

tree = ast.parse(source)

for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "create_reseller_sale":
        print("=" * 70)
        print(" FONCTION create_reseller_sale")
        print("=" * 70)
        print(f"LIGNES : {node.lineno} -> {node.end_lineno}")
        print()
        lines = source.splitlines()
        for number in range(node.lineno, node.end_lineno + 1):
            print(f"{number:4} | {lines[number - 1]}")
        break
else:
    print("CREATE_RESELLER_SALE=NOT_FOUND")