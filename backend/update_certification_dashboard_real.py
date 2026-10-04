from pathlib import Path

print("=== MISE A JOUR DASHBOARD CERTIFICATION REEL NSIKAY ===")


path = Path("dashboard/views.py")

content = path.read_text(encoding="utf-8")


old = """
def certification_stats(request):
    return JsonResponse({
        "module": "Certification NSIKAY",
        "total": 0,
        "certifications": []
    })
"""


new = """
def certification_stats(request):

    from certification.models import NSIKAYCertification

    certifications = []

    for cert in NSIKAYCertification.objects.all():

        certifications.append({

            "id": cert.id,

            "type": cert.certification_type,

            "activite": cert.activity,

            "document": cert.document_reference,

            "statut": cert.status,

            "proprietaire":
                cert.owner.username if cert.owner else None

        })


    return JsonResponse({

        "module": "Certification Centrale NSIKAY",

        "total":
            len(certifications),

        "certifications":
            certifications

    })
"""


if old in content:

    content = content.replace(old,new)

else:

    print("Ancienne fonction non trouvée, ajout manuel nécessaire")


path.write_text(content, encoding="utf-8")


print("=== DASHBOARD CERTIFICATION CONNECTE ===")