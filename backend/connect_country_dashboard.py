from pathlib import Path

print("=== CONNEXION SUPERVISION PAYS NSIKAY ===")

views = Path("dashboard/views.py")

content = views.read_text(encoding="utf-8")

if "def dashboard_pays" not in content:

    addition = r'''

# =====================================================
# DASHBOARD SUPERVISION PAYS NSIKAY
# =====================================================

from administration.models import CountrySupervisionDetail


def dashboard_pays(request):

    pays = CountrySupervisionDetail.objects.all()

    result = []

    for item in pays:

        result.append({

            "id": item.id,

            "pays": item.pays,

            "code_iso":
            item.code_iso,

            "actif":
            item.actif,

            "banques":
            item.banques_autorisees.count(),

            "devises":
            item.devises_autorisees,

            "conformite":
            item.niveau_conformite

        })


    return JsonResponse({

        "module":
        "Supervision Pays NSIKAY",

        "total":
        pays.count(),

        "pays":
        result

    })

'''

    content += addition

    views.write_text(content, encoding="utf-8")


print("=== DASHBOARD PAYS CONNECTE ===")