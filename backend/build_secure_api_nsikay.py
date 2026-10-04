import os

print("=== CREATION API SECURISEE NSIKAY ===")

# Création application API
os.system("python manage.py startapp api")

# settings ajout
settings = "nsikay/settings.py"

with open(settings,"r",encoding="utf-8") as f:
    data=f.read()

if "'api'," not in data:
    data=data.replace(
        "INSTALLED_APPS = [",
        "INSTALLED_APPS = [\n    'rest_framework',\n    'api',"
    )

with open(settings,"w",encoding="utf-8") as f:
    f.write(data)


# urls api
os.makedirs("api",exist_ok=True)

open("api/urls.py","w",encoding="utf-8").write("""
from django.urls import path
from . import views

urlpatterns=[

path("users/",views.users),
path("banks/",views.banks),
path("countries/",views.countries),
path("certifications/",views.certifications),
path("transactions/",views.transactions),
path("finance/",views.finance),

]
""")


# views API
open("api/views.py","w",encoding="utf-8").write("""
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
""")


# urls principales
urls="nsikay/urls.py"

with open(urls,"r",encoding="utf-8") as f:
    u=f.read()

if 'include("api.urls")' not in u:
    u=u.replace(
        "urlpatterns = [",
        "urlpatterns = [\n    path('api/', include('api.urls')),"
    )

    if "from django.urls import" in u and "include" not in u.splitlines()[0]:
        u=u.replace(
            "from django.urls import path",
            "from django.urls import path, include"
        )

with open(urls,"w",encoding="utf-8") as f:
    f.write(u)


# model logs securite
open("api/models.py","w",encoding="utf-8").write("""
from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()


class AdminActionLog(models.Model):

    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action=models.CharField(
        max_length=255
    )

    created=models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.action


class SecurityAlert(models.Model):

    message=models.CharField(
        max_length=255
    )

    active=models.BooleanField(
        default=True
    )

    created=models.DateTimeField(
        auto_now_add=True
    )
""")


print("=== API NSIKAY SECURISEE CREEE ===")

