import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

django.setup()


from django.contrib.auth import get_user_model
from administration.models import NSIKAYAdminRole


print("=== CREATION ROLE SUPER ADMIN NSIKAY ===")


User = get_user_model()


user = User.objects.filter(
    username="admin_test_nsikay"
).first()


if user:

    role, created = NSIKAYAdminRole.objects.update_or_create(

        user=user,

        defaults={

            "role":
            "SUPER_ADMIN",

            "active":
            True

        }

    )


    print(
        "ROLE:",
        role.role
    )


else:

    print(
        "Utilisateur admin introuvable"
    )


print("=== FIN ===")