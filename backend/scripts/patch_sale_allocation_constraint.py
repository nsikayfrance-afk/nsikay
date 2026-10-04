from pathlib import Path
import ast

path = Path(r"C:\Users\DELL Technologies\Desktop\nsikay nante\backend\gift_resellers\models.py")

source = path.read_text(encoding="utf-8")
tree = ast.parse(source)

lines = source.splitlines(keepends=True)

sale_allocation = None

for node in tree.body:
    if isinstance(node, ast.ClassDef) and node.name == "SaleAllocation":
        sale_allocation = node
        break

if sale_allocation is None:
    raise RuntimeError("SALE_ALLOCATION_NOT_FOUND")

meta = None

for node in sale_allocation.body:
    if isinstance(node, ast.ClassDef) and node.name == "Meta":
        meta = node
        break

if meta is None:
    raise RuntimeError("META_NOT_FOUND")

meta_source = "".join(lines[meta.lineno - 1:meta.end_lineno])

print("META_TROUVE")
print(meta_source)

if "uniq_sale_allocation_type" in source:
    print("CONTRAINTE_DEJA_PRESENTE")
    raise SystemExit(0)

if "constraints" in meta_source:
    raise RuntimeError(
        "META_CONTIENT_DEJA_CONSTRAINTS_SANS_NOM_ATTENDU"
    )

# Ajout après ordering = ["id"]
ordering_line = None

for node in meta.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "ordering":
                ordering_line = node
                break
    if ordering_line is not None:
        break

if ordering_line is None:
    raise RuntimeError("ORDERING_NOT_FOUND")

insert_at = ordering_line.end_lineno

indent = "        "

new_lines = [
    indent + "constraints = [\n",
    indent + "    models.UniqueConstraint(\n",
    indent + '        fields=["sale", "allocation_type"],\n',
    indent + '        name="uniq_sale_allocation_type",\n',
    indent + "    ),\n",
    indent + "]\n",
]

lines[insert_at:insert_at] = new_lines

new_source = "".join(lines)

# Validation syntaxique avant écriture
ast.parse(new_source)

path.write_text(new_source, encoding="utf-8")

print()
print("CONTRAINTE_AJOUTEE=OK")
print("MODELE_MODIFIE=OK")