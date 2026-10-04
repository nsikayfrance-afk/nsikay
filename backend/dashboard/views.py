from .security import require_nsikay_role


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




@require_nsikay_role(['SUPER_ADMIN','COUNTRY_ADMIN'])
def dashboard_pays(request):

    from administration.models import (
        CountrySupervision,
        CountrySupervisionDetail,
        BankPartner
    )


    pays = []


    for country in CountrySupervision.objects.all():

        detail = None

        try:
            detail = CountrySupervisionDetail.objects.filter(
                country=country
            ).first()

        except:
            pass


        banques = []

        try:

            for bank in BankPartner.objects.filter(
                country=str(country)
            ):

                banques.append(bank.name)

        except:

            banques = []


        pays.append({

            "id":
                country.id,

            "pays":
                str(country),

            "statut":
                getattr(country, "status", "supervise"),

            "banques":
                banques,

            "certification_obligatoire":
                True,

            "details":

                {

                "devises":
                    getattr(detail, "currencies", [])
                    if detail else [],

                "services":
                    getattr(detail, "services", [])
                    if detail else []

                }

        })


    return JsonResponse({

        "module":
            "Supervision Pays Centrale NSIKAY",

        "total_pays":
            len(pays),

        "pays":
            pays

    })



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

        "module": "Statistiques FinanciÃ¨res NSIKAY",

        "devises": Currency.objects.count(),

        "taux_change": ExchangeRate.objects.count(),

        "portefeuilles": Wallet.objects.count(),

        "transactions_wallet": WalletTransaction.objects.count()

    })



@login_required
def dashboard_stats(request):

    from django.contrib.auth import get_user_model

    User = get_user_model()

    return JsonResponse({

        "module": "NSIKAY Dashboard Statistics",

        "utilisateurs": User.objects.count(),

        "statut": "connecte"

    })



# === ALIASES COMPATIBILITE URLS NSIKAY ===

@login_required




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


def supervision_pays(request):
    return dashboard_pays(request)


@login_required
def certification_dashboard(request):
    return dashboard_certification(request)


@login_required
def transactions_dashboard(request):
    return dashboard_transactions(request)


@login_required
def finance_dashboard(request):
    return dashboard_finance(request)



# === COMPATIBILITE ANCIENS ENDPOINTS DASHBOARD NSIKAY ===

@login_required


@require_nsikay_role(['SUPER_ADMIN','CERTIFICATION_ADMIN'])
def certification_stats(request):

    from django.http import JsonResponse

    from certification.models import NSIKAYCertification


    certifications=[]


    for cert in NSIKAYCertification.objects.all():

        certifications.append({

            "id":cert.id,
            "utilisateur":cert.owner.username,
            "type":cert.certification_type,
            "activite":cert.activity,
            "statut":cert.status

        })


    return JsonResponse({

        "module":"Certification NSIKAY",

        "total":len(certifications),

        "certifications":certifications

    })



@require_nsikay_role(['SUPER_ADMIN','FINANCE_ADMIN','BANK_ADMIN'])
def transaction_stats(request):
    return dashboard_transactions(request)


@login_required


@require_nsikay_role(['SUPER_ADMIN','FINANCE_ADMIN'])
def finance_stats(request):

    from finance.models import Currency, ExchangeRate
    from banking.models import Wallet


    devises = []

    for currency in Currency.objects.all():

        devises.append({

            "code":
                getattr(currency, "code", str(currency)),

            "nom":
                str(currency)

        })


    taux = []

    for rate in ExchangeRate.objects.all():

        taux.append({

            "id":
                rate.id,

            "taux":
                getattr(rate, "rate", None),

            "source":
                str(rate)

        })


    wallets = []

    try:

        for wallet in Wallet.objects.all():

            wallets.append({

                "id":
                    wallet.id,

                "proprietaire":
                    str(getattr(wallet, "user", None)),

                "solde":
                    getattr(wallet, "balance", 0),

                "devise":
                    str(getattr(wallet, "currency", ""))

            })

    except Exception:

        wallets = []


    return JsonResponse({

        "module":
            "Finance RÃ©elle NSIKAY",

        "devises":
            len(devises),

        "liste_devises":
            devises,

        "taux_change":
            len(taux),

        "taux":
            taux,

        "portefeuilles":
            len(wallets),

        "wallets":
            wallets,

        "frais_NSIKAY":{

            "transfert":
                "0.25%",

            "retrait":
                "0.50%"

        }

    })


def pays_stats(request):
    return dashboard_pays(request)


@login_required
def banques_stats(request):
    return dashboard_banques(request)


@login_required
def dashboard_home(request):
    return dashboard_stats(request)



# === ALIASES COMPATIBILITE DASHBOARD NSIKAY ===

try:
    dashboard_stats
except NameError:
    def dashboard_stats(request):
        return stats_dashboard(request)


try:
    banques_partenaires
except NameError:
    def banques_partenaires(request):
        return bank_dashboard(request)


try:
    certification_stats
except NameError:
    @require_nsikay_role(['SUPER_ADMIN','CERTIFICATION_ADMIN'])
    def certification_stats(request):
        return certification_dashboard(request)


try:
    transactions_stats
except NameError:
    def transactions_stats(request):
        return transaction_stats(request)


try:
    finance_stats
except NameError:
    @require_nsikay_role(['SUPER_ADMIN','FINANCE_ADMIN'])
    def finance_stats(request):
        return finance_dashboard(request)


print("=== ALIASES DASHBOARD NSIKAY FINALISES ===")



@require_nsikay_role(['SUPER_ADMIN'])
def nsikay_control_center(request):

    from django.contrib.auth import get_user_model

    from administration.models import (
        BankPartner,
        CountrySupervision
    )

    from certification.models import NSIKAYCertification

    from transactions.models import Transaction


    User = get_user_model()


    data = {


        "module":
            "Centre Controle Central NSIKAY",


        "utilisateurs":
            User.objects.count(),


        "banques_partenaires":
            BankPartner.objects.count(),


        "pays_supervises":
            CountrySupervision.objects.count(),


        "certifications":
            NSIKAYCertification.objects.count(),


        "transactions":
            Transaction.objects.count(),


        "systeme":{

            "certification_obligatoire":
                True,

            "supervision_active":
                True,

            "statut":
                "OPERATIONNEL"

        }

    }


    return JsonResponse(data)


