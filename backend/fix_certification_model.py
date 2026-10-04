from pathlib import Path

print("=== CORRECTION MODELE CERTIFICATION NSIKAY ===")

file = Path("certification/models.py")

content = file.read_text(encoding="utf-8")


if "class NSIKAYCertification" not in content:

    content += """

# =====================================================
# CERTIFICATION CENTRALE NSIKAY
# =====================================================

class NSIKAYCertification(models.Model):

    TYPES = [
        ("personne", "Personne"),
        ("entreprise", "Entreprise"),
        ("banque", "Banque"),
        ("agent", "Agent"),
        ("service", "Service"),
    ]

    type_certification = models.CharField(
        max_length=50,
        choices=TYPES
    )

    nom_entite = models.CharField(
        max_length=255
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    statut = models.CharField(
        max_length=50,
        default="en_attente"
    )

    date_expiration = models.DateField(
        null=True,
        blank=True
    )

    valide_par = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.nom_entite

"""

    file.write_text(content, encoding="utf-8")


print("=== MODELE CERTIFICATION NSIKAY FORCE ===")