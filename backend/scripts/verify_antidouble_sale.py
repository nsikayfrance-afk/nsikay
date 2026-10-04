from pathlib import Path
import ast

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\gift_resellers\services.py")
source = path.read_text(encoding="utf-8")
tree = ast.parse(source)

found = False

for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "create_reseller_sale":
        lines = source.splitlines()

        for number in range(node.lineno, node.end_lineno + 1):
            line = lines[number - 1]

            if "PROTECTION ANTI DOUBLE VENTE" in line:
                found = True

            if "status__in=(\"PENDING\", \"PAID\", \"SETTLED\")" in line:
                print("ACTIVE_STATUSES=OK")

            if "Cette unite cadeau possede deja une vente active." in line:
                print("ERROR_MESSAGE=OK")

if not found:
    raise SystemExit("ANTI_DOUBLE_PROTECTION=NOT_FOUND")

print("ANTI_DOUBLE_PROTECTION=OK")