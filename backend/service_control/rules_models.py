from django.db import models


class ServiceRule(models.Model):

    SERVICE_TYPES = [
        ("BANK", "Partenaire bancaire obligatoire"),
        ("INSURANCE", "Partenaire assurance obligatoire"),
        ("TELECOM", "Operateur telecom certifie"),
        ("EDUCATION", "Etablissement education certifie"),
        ("HEALTH", "Etablissement sante certifie"),
        ("JUSTICE", "Professionnel justice certifie"),
        ("REAL_ESTATE", "Validation immobilier"),
        ("BUSINESS", "Entreprise certifiee"),
        ("NONE", "Validation simple"),
    ]

    service = models.OneToOneField(
        "GlobalService",
        on_delete=models.CASCADE
    )

    rule_type = models.CharField(
        max_length=30,
        choices=SERVICE_TYPES,
        default="NONE"
    )

    description = models.TextField(
        blank=True
    )


    def __str__(self):
        return self.service.name

