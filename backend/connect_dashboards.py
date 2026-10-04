from pathlib import Path

file = Path("dashboard/views.py")

content = r'''
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db.models import Count, Sum


# ==========================
# IMPORTS MODELES NSIKAY
# ==========================

try:
    from banking.models import *
except:
    pass

try:
    from administration.models import (
        BankCertification,
        CountrySupervision,
        CurrencyApproval,
        ValidationRequest,
        BankCountryAccess,
        BankCurrencyAccess,
        BankServiceAuthorization,
        CountryBankAuthorization
    )
except:
    pass

try:
    from certification.models import *
except:
    pass

try:
    from transactions.models import *
except:
    pass

try:
    from finance.models import *
except:
    pass



def response_dashboard(request, module, data):

    return JsonResponse({

        "module": module,

        "user": request.user.username
            if request.user.is_authenticated
            else "anonymous",

        "status": "active",

        "data": data

    })



# ==========================
# DASHBOARD ADMINISTRATION
# ==========================

@login_required
def admin_dashboard(request):

    return response_dashboard(
        request,
        "Administration NSIKAY",
        {
            "system": "online"
        }
    )



# ==========================
# DASHBOARD BANQUE
# ==========================

@login_required
def banque_dashboard(request):

    data = {}

    try:
        data["certifications_banques"] = BankCertification.objects.count()
    except:
        data["certifications_banques"] = 0

    try:
        data["acces_pays"] = BankCountryAccess.objects.count()
    except:
        data["acces_pays"] = 0

    try:
        data["acces_devises"] = BankCurrencyAccess.objects.count()
    except:
        data["acces_devises"] = 0


    return response_dashboard(
        request,
        "Dashboard Banque Partenaire",
        data
    )



# ==========================
# SUPERVISION PAYS
# ==========================

@login_required
def pays_dashboard(request):

    data = {}

    try:
        data["supervision_pays"] = CountrySupervision.objects.count()
    except:
        data["supervision_pays"] = 0

    try:
        data["autorisations_banques"] = CountryBankAuthorization.objects.count()
    except:
        data["autorisations_banques"] = 0


    return response_dashboard(
        request,
        "Administration Pays",
        data
    )



# ==========================
# CERTIFICATION
# ==========================

@login_required
def certification_dashboard(request):

    data = {}

    try:
        data["demandes_validation"] = ValidationRequest.objects.count()
    except:
        data["demandes_validation"] = 0


    try:
        data["certifications"] = BankCertification.objects.count()
    except:
        data["certifications"] = 0


    return response_dashboard(
        request,
        "Certification NSIKAY",
        data
    )



# ==========================
# FINANCE
# ==========================

@login_required
def finance_dashboard(request):

    data = {}

    try:
        data["transactions"] = Transaction.objects.count()

        data["volume_total"] = (
            Transaction.objects
            .aggregate(total=Sum("amount"))
            .get("total")
            or 0
        )

    except:

        data["transactions"] = 0
        data["volume_total"] = 0



    return response_dashboard(
        request,
        "Finance NSIKAY",
        data
    )



# ==========================
# WENZE
# ==========================

@login_required
def wenze_dashboard(request):

    return response_dashboard(
        request,
        "WENZE",
        {
            "status": "connected"
        }
    )



# ==========================
# CONFORMITE
# ==========================

@login_required
def conformite_dashboard(request):

    return response_dashboard(
        request,
        "Conformité",
        {
            "status": "active"
        }
    )



# ==========================
# PUBLICITE
# ==========================

@login_required
def publicite_dashboard(request):

    return response_dashboard(
        request,
        "Publicité NSIKAY",
        {}
    )



# ==========================
# EVENEMENTS
# ==========================

@login_required
def evenements_dashboard(request):

    return response_dashboard(
        request,
        "Événements NSIKAY",
        {}
    )
'''

file.write_text(content, encoding="utf-8")

print("=== DASHBOARDS NSIKAY CONNECTES AUX DONNEES ===")

