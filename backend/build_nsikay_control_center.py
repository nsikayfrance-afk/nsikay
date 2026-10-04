from pathlib import Path

print("=== CREATION CENTRE CONTROLE NSIKAY ===")


path = Path("dashboard/views.py")

content = path.read_text(encoding="utf-8")


new_view = """

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

"""


if "def nsikay_control_center" not in content:

    content += new_view


path.write_text(content, encoding="utf-8")


# ajout URL

url_path = Path("dashboard/urls.py")

urls = url_path.read_text(encoding="utf-8")


if 'nsikay_control_center' not in urls:

    urls += """

from . import views

urlpatterns += [

    path(
        "control-center/",
        views.nsikay_control_center
    ),

]

"""


url_path.write_text(urls, encoding="utf-8")


print("=== CENTRE CONTROLE NSIKAY CREE ===")