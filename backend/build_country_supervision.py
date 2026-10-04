from pathlib import Path

print("=== CREATION SUPERVISION PAYS NSIKAY ===")

file = Path("administration/models.py")

content = file.read_text(encoding="utf-8")


if "class CountryCurrencyAccess" not in content:

    addition = """

# ===============================
# SUPERVISION PAYS NSIKAY
# ===============================


class CountryCurrencyAccess(models.Model):

    country = models.ForeignKey(
        CountrySupervision,
        on_delete=models.CASCADE
    )

    currency = models.CharField(
        max_length=10
    )

    active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.country} - {self.currency}"




class CountryRegulation(models.Model):

    country = models.OneToOneField(
        CountrySupervision,
        on_delete=models.CASCADE
    )

    authority = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    regulation_status = models.CharField(
        max_length=50,
        default="active"
    )


    def __str__(self):
        return str(self.country)



class CountryBankAccess(models.Model):

    country = models.ForeignKey(
        CountrySupervision,
        on_delete=models.CASCADE
    )

    bank = models.ForeignKey(
        "BankPartner",
        on_delete=models.CASCADE
    )

    authorized = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.country} - {self.bank}"

"""

    with file.open("a", encoding="utf-8") as f:
        f.write(addition)


print("=== MODELES SUPERVISION PAYS AJOUTES ===")