from api_nsikay.models import VirtualGift

print("")
print("=" * 70)
print("ETAT BASE VIRTUALGIFT")
print("=" * 70)

print("TABLE :", VirtualGift._meta.db_table)
print("OBJETS :", VirtualGift.objects.count())

print("")
print("CHAMPS ATTENDUS :")

for field in VirtualGift._meta.fields:
    print(
        f"- {field.name} "
        f"| {field.__class__.__name__} "
        f"| null={field.null} "
        f"| unique={field.unique}"
    )

print("=" * 70)