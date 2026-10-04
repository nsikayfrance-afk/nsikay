
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User=get_user_model()


def users(request):
    return JsonResponse({
        "module":"API Utilisateurs NSIKAY",
        "profils":User.objects.count(),
        "statuts":[
            "active",
            "verification",
            "bloque"
        ],
        "permissions":"actives"
    })


def banks(request):
    return JsonResponse({
        "module":"API Banques NSIKAY",
        "activation":True,
        "services":[
            "deposit",
            "withdraw",
            "transfer",
            "wallet"
        ],
        "devises":[
            "CDF",
            "USD",
            "EUR"
        ]
    })


def countries(request):
    return JsonResponse({
        "module":"API Pays NSIKAY",
        "supervision":True,
        "controle":"actif"
    })


def certifications(request):
    return JsonResponse({
        "module":"API Certification NSIKAY",
        "KYC":True,
        "documents":"validation",
        "alertes":True
    })


def transactions(request):
    return JsonResponse({
        "module":"API Transactions NSIKAY",
        "historique":True,
        "transferts":True,
        "controle":True
    })


def finance(request):
    return JsonResponse({
        "module":"API Finance NSIKAY",
        "wallet":True,
        "solde_reel":True,
        "statistiques":True,
        "graphiques":True
    })
