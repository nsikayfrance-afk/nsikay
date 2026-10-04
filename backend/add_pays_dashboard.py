from pathlib import Path

file = Path("dashboard/views.py")

content = file.read_text(encoding="utf-8")

extra = '''

from administration.models import (
    CountrySupervision,
    BankCountryAccess,
    BankCurrencyAccess,
    CurrencyApproval,
    ValidationRequest
)


@login_required
def pays_stats(request):

    data = {

        "pays":
            CountrySupervision.objects.count(),

        "acces_banques":
            BankCountryAccess.objects.count(),

        "acces_devises":
            BankCurrencyAccess.objects.count(),

        "approbations_devises":
            CurrencyApproval.objects.count(),

        "validations":
            ValidationRequest.objects.count(),

    }


    return JsonResponse({

        "dashboard":
            "Administration Pays NSIKAY",

        "user":
            request.user.username,

        "stats":
            data

    })

'''

if "def pays_stats" not in content:
    file.write_text(content + extra, encoding="utf-8")

print("=== DASHBOARD ADMINISTRATION PAYS AJOUTE ===")

