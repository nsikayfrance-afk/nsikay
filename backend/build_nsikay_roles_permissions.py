from pathlib import Path

print("=== CREATION ROLES ADMIN NSIKAY ===")


path = Path("administration/models.py")


content = path.read_text(encoding="utf-8")


model = """


from django.conf import settings
from django.db import models


class NSIKAYAdminRole(models.Model):

    ROLE_CHOICES = [

        ("SUPER_ADMIN", "Super Administrateur NSIKAY"),

        ("BANK_ADMIN", "Administrateur Banque"),

        ("COUNTRY_ADMIN", "Administrateur Pays"),

        ("CERTIFICATION_ADMIN", "Administrateur Certification"),

        ("FINANCE_ADMIN", "Administrateur Finance"),

    ]


    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )


    active = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return f"{self.user} - {self.role}"



class NSIKAYPermission(models.Model):


    role = models.ForeignKey(
        NSIKAYAdminRole,
        on_delete=models.CASCADE
    )


    module = models.CharField(
        max_length=100
    )


    can_view = models.BooleanField(
        default=False
    )


    can_create = models.BooleanField(
        default=False
    )


    can_update = models.BooleanField(
        default=False
    )


    can_delete = models.BooleanField(
        default=False
    )


    def __str__(self):

        return self.module

"""


if "class NSIKAYAdminRole" not in content:

    content += model


path.write_text(content, encoding="utf-8")


print("=== MODELES ROLES AJOUTES ===")