from gift_resellers.models import GiftResellerAuditLog

print("")
print("============================================================")
print(" INSPECTION GiftResellerAuditLog.action")
print("============================================================")

print("ATTRIBUT Action :", hasattr(GiftResellerAuditLog, "Action"))

field = GiftResellerAuditLog._meta.get_field("action")

print("TYPE :", field.__class__.__name__)
print("DEFAULT :", field.default)
print("CHOICES :")

for choice in field.choices:
    print(" ", choice)

print("")
print("============================================================")