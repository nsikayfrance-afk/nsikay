from django.shortcuts import render, redirect

from .models import (
    BankCertification,
    CurrencyApproval,
    PartnerCertification,
    CountrySupervision
)



def admin_dashboard(request):

    return render(

        request,

        "administration/dashboard.html",

        {

            "banks":
            BankCertification.objects.all(),

            "currencies":
            CurrencyApproval.objects.all(),

            "partners":
            PartnerCertification.objects.all(),

            "countries":
            CountrySupervision.objects.all(),

        }

    )




def approve_bank(request,id):

    item = BankCertification.objects.get(id=id)

    item.status="approved"

    item.save()

    return redirect("admin_dashboard")




def approve_currency(request,id):

    item = CurrencyApproval.objects.get(id=id)

    item.status="approved"

    item.currency.approved=True

    item.currency.save()

    item.save()

    return redirect("admin_dashboard")




def approve_partner(request,id):

    item = PartnerCertification.objects.get(id=id)

    item.status="approved"

    item.save()

    return redirect("admin_dashboard")

