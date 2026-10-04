from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

extra = '''

from certification.models import (
    CertificationAgent,
    FieldInspection,
    CertificationCertificate
)


@login_required
def certification_stats(request):

    data = {

        "agents":
            CertificationAgent.objects.count(),

        "inspections":
            FieldInspection.objects.count(),

        "certificats":
            CertificationCertificate.objects.count(),

    }


    return JsonResponse({

        "dashboard":
            "Autorite de Certification NSIKAY",

        "user":
            request.user.username,

        "stats":
            data

    })

'''

if "def certification_stats" not in content:
    file.write_text(content + extra, encoding="utf-8")

print("=== DASHBOARD CERTIFICATION AJOUTE ===")

