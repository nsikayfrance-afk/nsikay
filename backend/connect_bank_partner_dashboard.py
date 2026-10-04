from pathlib import Path

print("=== CONNEXION DASHBOARD BANQUES PARTENAIRES NSIKAY ===")

views = Path("dashboard/views.py")

content = views.read_text(encoding="utf-8")

if "def banques_partenaires" not in content:

    addition = r'''

# =====================================================
# DASHBOARD BANQUES PARTENAIRES NSIKAY
# =====================================================

from administration.models import (
    BankPartner,
    BankPartnerCurrency,
    BankPartnerService
)


def banques_partenaires(request):

    banques = BankPartner.objects.all()

    data = []

    for banque in banques:

        devises = BankPartnerCurrency.objects.filter(
            bank=banque
        ).count()

        services = BankPartnerService.objects.filter(
            bank=banque
        ).count()

        data.append({
            "id": banque.id,
            "nom": str(banque),
            "devises": devises,
            "services": services,
            "statut": getattr(
                banque,
                "status",
                "actif"
            )
        })

    return JsonResponse({

        "module":
        "Banques Partenaires NSIKAY",

        "total":
        banques.count(),

        "banques":
        data

    })


'''

    content += addition

    views.write_text(content, encoding="utf-8")


print("=== DASHBOARD BANQUES CONNECTE AUX DONNEES REELLES ===")