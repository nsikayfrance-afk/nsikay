from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_ROOT = BASE_DIR / "media"


STORAGES = {

    "default": {

        "BACKEND":
        "django.core.files.storage.FileSystemStorage"

    },


    "staticfiles": {

        "BACKEND":
        "whitenoise.storage.CompressedManifestStaticFilesStorage"

    }

}


# NSIKAY - TARIFICATION STOCKAGE
# 10 GB = 10 EUR
# 100 GB = 50 EUR
