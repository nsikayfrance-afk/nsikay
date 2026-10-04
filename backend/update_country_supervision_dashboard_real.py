from pathlib import Path

print("=== CONNEXION SUPERVISION PAYS REELLE NSIKAY ===")


path = Path("dashboard/views.py")

content = path.read_text(encoding="utf-8")


start = content.find("def dashboard_pays")

if start != -1:

    end = content.find("\ndef ", start + 5)

    if end == -1:
        end = len(content)


    old = content[start:end]


    new = """

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


"""


    content = content.replace(old,new)

else:

    print("fonction dashboard_pays introuvable")


path.write_text(content, encoding="utf-8")


print("=== SUPERVISION PAYS CONNECTEE ===")