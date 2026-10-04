from pathlib import Path

print("=== CREATION MODULE BANQUES PARTENAIRES NSIKAY ===")

models = Path("administration/models.py")

content = models.read_text(encoding="utf-8")

if "class BankPartner" not in content:

    addition = """

# ================================
# BANQUES PARTENAIRES NSIKAY
# ================================

from django.db import models


class BankPartner(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True
    )

    country = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    certified = models.BooleanField(
        default=False
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.name



class BankPartnerCurrency(models.Model):

    bank = models.ForeignKey(
        BankPartner,
        on_delete=models.CASCADE
    )

    currency = models.CharField(
        max_length=10
    )

    active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.bank} - {self.currency}"



class BankPartnerService(models.Model):

    SERVICES = [
        ("deposit","Dépôt"),
        ("withdraw","Retrait"),
        ("transfer","Transfert"),
        ("exchange","Change"),
        ("wallet","Wallet"),
    ]


    bank = models.ForeignKey(
        BankPartner,
        on_delete=models.CASCADE
    )

    service = models.CharField(
        max_length=50,
        choices=SERVICES
    )

    active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.bank} - {self.service}"

"""

    with models.open("a",encoding="utf-8") as f:
        f.write(addition)


print("=== MODELES BANQUES PARTENAIRES AJOUTES ===")