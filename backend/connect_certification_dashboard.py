from pathlib import Path

print("=== CONNEXION CERTIFICATION DASHBOARD NSIKAY ===")

views = Path("dashboard/views.py")

content = views.read_text(encoding="utf-8")

if "def certification_stats" not in content:

    content += r'''

# =====================================================
# DASHBOARD CERTIFICATION NSIKAY
# =====================================================

from certification.models import NSIKAYCertification


def certification_stats(request):

    certifications = NSIKAYCertification.objects.all()


    valides = certifications.filter(
        statut="valide"
    ).count()


    attente = certifications.filter(
        statut="en_attente"
    ).count()


    expirees = certifications.filter(
        statut="expire"
    ).count()


    domaines = {}

    for cert in certifications:

        type_cert = cert.type_certification

        domaines[type_cert] = (
            domaines.get(type_cert, 0) + 1
        )


    return JsonResponse({

        "module":
        "Certification NSIKAY",

        "total":
        certifications.count(),

        "valides":
        valides,

        "en_attente":
        attente,

        "expirees":
        expirees,

        "domaines":
        domaines

    })

'''

    views.write_text(content, encoding="utf-8")


print("=== DASHBOARD CERTIFICATION CONNECTE ===")