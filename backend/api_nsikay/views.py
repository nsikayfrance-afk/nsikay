# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SecureAPIView(APIView):
    permission_classes=[IsAuthenticated]


class UsersAPI(SecureAPIView):
    def get(self,request):
        return Response({
            "module":"UTILISATEURS",
            "status":"active",
            "features":[
                "profils",
                "statuts",
                "verification",
                "permissions"
            ]
        })


class BanksAPI(SecureAPIView):
    def get(self,request):
        return Response({
            "module":"BANQUES",
            "services":[
                "activation",
                "deactivation",
                "devises",
                "suivi activité"
            ]
        })


class CertificationAPI(SecureAPIView):
    def get(self,request):
        return Response({
            "module":"CERTIFICATION",
            "features":[
                "KYC",
                "documents",
                "validation",
                "alertes"
            ]
        })


class WalletAPI(SecureAPIView):
    def get(self,request):
        return Response({
            "module":"WALLET",
            "features":[
                "solde réel",
                "dépôt",
                "retrait",
                "transfert",
                "historique"
            ]
        })


class FinanceAPI(SecureAPIView):
    def get(self,request):
        return Response({
            "module":"FINANCE",
            "features":[
                "statistiques",
                "volumes",
                "croissance",
                "rapports"
            ]
        })

# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def countries_list(request):

    countries = [
        {
            "code": "CD",
            "name": "République Démocratique du Congo",
            "currency": "CDF"
        },
        {
            "code": "US",
            "name": "United States",
            "currency": "USD"
        },
        {
            "code": "EU",
            "name": "European Union",
            "currency": "EUR"
        }
    ]

    return Response({
        "success": True,
        "module": "NSIKAY COUNTRIES API",
        "countries": countries
    })

# === API NSIKAY VIEWS COMPATIBILITE ===

from django.http import JsonResponse


def banks_list(request):
    return JsonResponse({
        "module": "banks",
        "status": "active",
        "data": []
    })


def transactions_list(request):
    return JsonResponse({
        "module": "transactions",
        "status": "active",
        "data": []
    })


def certification_list(request):
    return JsonResponse({
        "module": "certification",
        "status": "active",
        "data": []
    })


def finance_dashboard(request):
    return JsonResponse({
        "module": "finance",
        "status": "active",
        "data": {}
    })


def wallet_dashboard(request):
    return JsonResponse({
        "module": "wallet",
        "status": "active",
        "balance": 0,
        "currency": "USD"
    })


def kyc_status(request):
    return JsonResponse({
        "module": "KYC",
        "status": "pending"
    })


print("=== API NSIKAY VIEWS COMPATIBILITE CHARGEES ===")


# Wallet compatibility API

from django.http import JsonResponse


def wallet_balance(request):

    return JsonResponse(
        {
            "platform": "NSIKAY",
            "wallet": "active",
            "currencies": [
                "USD",
                "EUR",
                "CDF"
            ],
            "status": "ready"
        }
    )


