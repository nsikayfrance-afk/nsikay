from pathlib import Path

file = Path("dashboard/views.py")

content = """

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from administration.models import (
    CountrySupervision,
    BankCountryAccess,
    BankCurrencyAccess,
    BankServiceAuthorization
)

from certification.models import *
from transactions.models import *
from finance.models import *


@login_required
def dashboard_banques(request):

    banques = []

    for bank in BankServiceAuthorization.objects.all():

        banques.append({
            "id": bank.id,
            "banque": str(bank),
            "statut": "active"
        })


    return JsonResponse({

        "module": "Banques Partenaires NSIKAY",

        "total": len(banques),

        "banques": banques

    })



@login_required
def dashboard_pays(request):

    pays = []

    for item in CountrySupervision.objects.all():

        pays.append({

            "id": item.id,

            "pays": str(item),

            "statut": "supervise"

        })


    return JsonResponse({

        "module": "Supervision Pays NSIKAY",

        "total": len(pays),

        "pays": pays

    })



@login_required
def dashboard_certification(request):

    certifications = []

    try:

        for cert in BankCertification.objects.all():

            certifications.append({

                "id": cert.id,

                "certification": str(cert)

            })

    except:

        pass


    return JsonResponse({

        "module": "Certification NSIKAY",

        "total": len(certifications),

        "certifications": certifications

    })



@login_required
def dashboard_transactions(request):

    try:

        total = Transaction.objects.count()

    except:

        total = 0


    return JsonResponse({

        "module": "Transactions NSIKAY",

        "total_transactions": total

    })



@login_required
def dashboard_finance(request):

    return JsonResponse({

        "module": "Statistiques Financières NSIKAY",

        "devises": Currency.objects.count(),

        "taux_change": ExchangeRate.objects.count(),

        "portefeuilles": Wallet.objects.count(),

        "transactions_wallet": WalletTransaction.objects.count()

    })

"""

file.write_text(content, encoding="utf-8")

print("=== DASHBOARDS DONNEES REELLES NSIKAY MIS A JOUR ===")


