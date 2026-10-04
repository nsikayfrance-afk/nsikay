from pathlib import Path

file = Path("administration/admin.py")

content = file.read_text(encoding="utf-8")


if "CountryCurrencyAccess" not in content:

    with file.open("a", encoding="utf-8") as f:

        f.write("""

from .models import (
    CountryCurrencyAccess,
    CountryRegulation,
    CountryBankAccess
)

admin.site.register(CountryCurrencyAccess)
admin.site.register(CountryRegulation)
admin.site.register(CountryBankAccess)

""")


print("=== ADMIN SUPERVISION PAYS AJOUTE ===")