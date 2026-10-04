from pathlib import Path

admin = Path("administration/admin.py")

content = admin.read_text(encoding="utf-8")

if "BankPartner" not in content:

    with admin.open("a",encoding="utf-8") as f:

        f.write("""

from .models import (
    BankPartner,
    BankPartnerCurrency,
    BankPartnerService
)

admin.site.register(BankPartner)
admin.site.register(BankPartnerCurrency)
admin.site.register(BankPartnerService)

""")

print("=== ADMIN BANQUES AJOUTE ===")