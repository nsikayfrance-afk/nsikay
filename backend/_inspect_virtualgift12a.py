from api_nsikay.models import VirtualGift

print("")
print("=" * 70)
print("MODELE DJANGO VIRTUALGIFT")
print("=" * 70)

print("TABLE :", VirtualGift._meta.db_table)

print("")
print("CHAMPS :")

for field in VirtualGift._meta.fields:

    print(
        f"{field.name} | "
        f"{field.__class__.__name__} | "
        f"null={field.null} | "
        f"blank={field.blank} | "
        f"unique={field.unique} | "
        f"default={field.default!r}"
    )

print("")
print(
    "NOMBRE OBJETS :",
    VirtualGift.objects.count()
)

print("=" * 70)