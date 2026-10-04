from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import OnlineBankAccountRequest


def bank_dashboard(request):

    return JsonResponse({

        "comptes_en_attente":
        OnlineBankAccountRequest.objects.filter(
            status="pending"
        ).count(),

        "comptes_actifs":
        OnlineBankAccountRequest.objects.filter(
            status="active"
        ).count(),

        "actions":[

            "Accepter demande",

            "Refuser demande",

            "Activer compte",

            "Consulter rapports"

        ]

    })



def accept_account(request, account_id):

    account = get_object_or_404(
        OnlineBankAccountRequest,
        id=account_id
    )


    account.status = "approved"

    account.save()


    return JsonResponse({

        "message":
        "Compte accepté"

    })



def activate_account(request, account_id):

    account = get_object_or_404(
        OnlineBankAccountRequest,
        id=account_id
    )


    account.status = "active"

    account.save()


    return JsonResponse({

        "message":
        "Compte activé officiellement"

    })



def reject_account(request, account_id):

    account = get_object_or_404(
        OnlineBankAccountRequest,
        id=account_id
    )


    account.status = "rejected"

    account.save()


    return JsonResponse({

        "message":
        "Compte refusé"

    })

