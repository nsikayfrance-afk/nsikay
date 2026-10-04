from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import (
    PartnerApplication,
    PartnerCertification,
    PartnerSupply,
)



@login_required
def partner_dashboard(request):

    partner = PartnerApplication.objects.filter(
        user=request.user
    ).first()


    if not partner:

        return JsonResponse({

            "status":"error",

            "message":
            "Aucun profil partenaire trouvé"

        })


    return JsonResponse({

        "partner":
        partner.business_name,

        "status":
        partner.status,

        "message":
        "Dashboard partenaire actif"

    })



@login_required
def request_certification(request):

    partner = PartnerApplication.objects.filter(user=request.user).first()


    partner.status = "certification"

    partner.save()


    PartnerCertification.objects.get_or_create(
        partner=partner
    )


    return JsonResponse({

        "status":"success",

        "message":
        "Demande de certification envoyée"

    })



@login_required
def request_supply(request):

    partner = PartnerApplication.objects.filter(user=request.user).first()


    amount = request.GET.get(
        "amount"
    )


    currency = request.GET.get(
        "currency"
    )


    return JsonResponse({

        "status":
        "pending",

        "partner":
        partner.business_name,

        "amount":
        amount,

        "currency":
        currency,

        "message":
        "Demande envoyée à la banque"

    })

