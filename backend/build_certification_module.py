from pathlib import Path

print("=== CREATION CERTIFICATION NSIKAY COMPLETE ===")

file = Path("certification/models.py")

content = file.read_text(encoding="utf-8")


if "class NSIKAYCertification" not in content:

    addition = """

from django.db import models
from django.conf import settings


class NSIKAYCertification(models.Model):

    TYPE_CHOICES = [

        ("person","Personne"),
        ("company","Entreprise"),
        ("agent","Agent"),
        ("bank","Banque"),
        ("partner","Partenaire"),

    ]


    STATUS_CHOICES = [

        ("pending","En attente"),
        ("approved","Validée"),
        ("rejected","Refusée"),
        ("expired","Expirée"),

    ]


    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


    certification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )


    activity = models.CharField(
        max_length=255
    )


    document_reference = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )


    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return f"{self.owner} - {self.certification_type}"



class CertificationHistory(models.Model):

    certification = models.ForeignKey(
        NSIKAYCertification,
        on_delete=models.CASCADE
    )


    old_status = models.CharField(
        max_length=50
    )


    new_status = models.CharField(
        max_length=50
    )


    comment = models.TextField(
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return str(self.certification)

"""

    with file.open("a", encoding="utf-8") as f:
        f.write(addition)


print("=== MODELES CERTIFICATION CREES ===")