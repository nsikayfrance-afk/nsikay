from pathlib import Path

file = Path("administration/models.py")

content = file.read_text(encoding="utf-8")

if "class BankCountryAccess" not in content:

    content += """



class BankCountryAccess(models.Model):

    bank_name = models.CharField(
        max_length=255
    )

    country_name = models.CharField(
        max_length=255
    )

    access_level = models.CharField(
        max_length=100,
        default="STANDARD"
    )

    status = models.CharField(
        max_length=50,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.bank_name} - {self.country_name}"
"""

    file.write_text(content, encoding="utf-8")

print("=== BankCountryAccess AJOUTE ===")

