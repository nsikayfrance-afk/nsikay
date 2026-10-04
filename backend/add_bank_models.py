from pathlib import Path

file = Path("administration/models.py")

content = file.read_text(encoding="utf-8")

models = """



class BankCurrencyAccess(models.Model):

    bank_name = models.CharField(
        max_length=255
    )

    currency = models.CharField(
        max_length=50
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
        return f"{self.bank_name} - {self.currency}"



class BankServiceAuthorization(models.Model):

    bank_name = models.CharField(
        max_length=255
    )

    service_name = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=50,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.bank_name} - {self.service_name}"



class CountryBankAuthorization(models.Model):

    country_name = models.CharField(
        max_length=255
    )

    bank_name = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=50,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.country_name} - {self.bank_name}"

"""

for name in [
    "BankCurrencyAccess",
    "BankServiceAuthorization",
    "CountryBankAuthorization"
]:
    if f"class {name}" not in content:
        content += models

file.write_text(content, encoding="utf-8")

print("=== MODELES BANQUE ADMINISTRATION AJOUTES ===")

