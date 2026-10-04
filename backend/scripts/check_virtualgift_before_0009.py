import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from api_nsikay.models import VirtualGift

count = VirtualGift.objects.count()

print("")
print("VirtualGift existants :", count)

if count != 0:
    raise RuntimeError(
        "La table VirtualGift n'est pas vide. "
        "La migration manuelle 0009 doit être revue avant application."
    )