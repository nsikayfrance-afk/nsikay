from django.db import connection

print("")
print("=" * 60)
print("DIAGNOSTIC BASE DJANGO")
print("=" * 60)
print("ENGINE :", connection.settings_dict.get("ENGINE"))
print("VENDOR :", connection.vendor)
print("NAME   :", connection.settings_dict.get("NAME"))
print("=" * 60)
