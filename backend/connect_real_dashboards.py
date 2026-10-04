from pathlib import Path

file = Path("dashboard/views.py")

content = """

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count


# ================================
# DASHBOARD DONNEES GENERALES
# ================================

@login_required
def dashboard_stats(request):

    from django.contrib.auth import get_user_model

    User = get_user_model()

    return JsonResponse({

        "module": "NSIKAY Dashboard Statistics",

        "utilisateurs": User.objects.count(),

        "statut": "connecte",

    })


# ================================
# BANQUES PARTENAIRES
# ================================

@login_required
def banques_partenaires(request):

    from administration.models import BankServiceAuthorization

    banques = []

    for banque in BankServiceAuthorization.objects.all():

        banques.append({

            "id": banque.id,

            "banque": str(banque),

            "statut": "active"

        })


    return JsonResponse({

        "module": "Banques Partenaires NSIKAY",

        "total": len(banques),

        "banques": banques

    })


# ================================
# SUPERVISION PAYS
# ================================

@login_required
def supervision_pays(request):

    from administration.models import CountrySupervision


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



# ================================
# CERTIFICATION
# ================================

@login_required
def certification_stats(request):

    from administration.models import BankCertification


    certifications = BankCertification.objects.count()


    return JsonResponse({

        "module": "Certification NSIKAY",

        "certifications": certifications

    })



# ================================
# TRANSACTIONS
# ================================

@login_required
def transactions_stats(request):

    try:

        from transactions.models import Transaction


        total = Transaction.objects.count()


        return JsonResponse({

            "module": "Transactions NSIKAY",

            "total_transactions": total

        })


    except Exception:


        return JsonResponse({

            "module": "Transactions NSIKAY",

            "total_transactions": 0

        })



# ================================
# FINANCE
# ================================

@login_required
def finance_stats(request):

    try:

        from finance.models import *


        return JsonResponse({

            "module": "Statistiques Financières NSIKAY",

            "status": "connecte"

        })


    except Exception:


        return JsonResponse({

            "module": "Statistiques Financières NSIKAY",

            "status": "initialisation"

        })

"""

file.write_text(content, encoding="utf-8")


print("=== DASHBOARDS DONNEES NSIKAY AJOUTES ===")


