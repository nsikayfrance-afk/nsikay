from pathlib import Path

print("=== MODULE SUPERVISION PAYS NSIKAY ===")

models = Path("administration/models.py")

content = models.read_text(encoding="utf-8")

if "class CountrySupervisionDetail" not in content:

    content += r'''

# =====================================================
# SUPERVISION PAYS NSIKAY
# =====================================================

class CountrySupervisionDetail(models.Model):

    pays = models.CharField(max_length=100)

    code_iso = models.CharField(
        max_length=10,
        unique=True
    )

    actif = models.BooleanField(
        default=True
    )

    banques_autorisees = models.ManyToManyField(
        "BankPartner",
        blank=True
    )

    devises_autorisees = models.JSONField(
        default=list
    )

    niveau_conformite = models.CharField(
        max_length=50,
        default="en_verification"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.pays

'''

    models.write_text(content, encoding="utf-8")


print("=== MODELE SUPERVISION PAYS AJOUTE ===")