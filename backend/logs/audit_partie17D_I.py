import os
import sys

backend_path = os.getcwd()

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings",
)

import django

django.setup()

from nsikay_activities.models import Activity
from certification.models import (
    NSIKAYCertification,
    CertificationHistory,
)

print(
    "ACTIVITES_TOTAL=",
    Activity.objects.count(),
)

print(
    "CERTIFICATIONS_TOTAL=",
    NSIKAYCertification.objects.count(),
)

print(
    "CERTIFICATIONS_TYPE_ACTIVITY=",
    NSIKAYCertification.objects.filter(
        certification_type="activity",
    ).count(),
)

print(
    "HISTORIQUES_TOTAL=",
    CertificationHistory.objects.count(),
)

print(
    "ACTIVITES_AVEC_CERTIFICATION=",
    Activity.objects.filter(
        nsikay_certification__isnull=False,
    ).count(),
)
