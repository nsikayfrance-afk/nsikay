from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")


if "def banques_partenaires" in content:

    start = content.index("def banques_partenaires")
    
    end = content.find("\ndef ", start + 5)

    if end == -1:
        end = len(content)


    new_code = r'''

def banques_partenaires(request):

    from django.http import JsonResponse
    from administration.models import (
        BankPartner,
        BankPartnerCurrency,
        BankPartnerService
    )

    banques = []

    for bank in BankPartner.objects.all():

        devises = list(
            BankPartnerCurrency.objects.filter(
                bank=bank,
                active=True
            ).values_list(
                "currency",
                flat=True
            )
        )

        services = list(
            BankPartnerService.objects.filter(
                bank=bank,
                active=True
            ).values_list(
                "service",
                flat=True
            )
        )


        banques.append({

            "id": bank.id,
            "nom": bank.name,
            "pays": bank.country,
            "code": bank.code,
            "certifiee": bank.certified,
            "active": bank.active,
            "devises": devises,
            "services": services

        })


    return JsonResponse({

        "module": "Banques Partenaires NSIKAY",
        "total": len(banques),
        "banques": banques

    })

'''

    content = content[:start] + new_code + content[end:]

    file.write_text(content, encoding="utf-8")


print("=== DASHBOARD BANQUES CONNECTE AUX DONNEES REELLES ===")