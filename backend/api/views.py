from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer, RegisterSerializer


User = get_user_model()


# ============================================================
# AUTHENTIFICATION
# ============================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user = serializer.save()

    token = Token.objects.create(user=user)

    return Response(
        {
            "success": True,
            "message": "Compte NSIKAY créé avec succès.",
            "token": token.key,
            "user": UserSerializer(user).data,
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {
                "success": False,
                "message": "Nom d'utilisateur et mot de passe obligatoires."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(
        request=request,
        username=username,
        password=password
    )

    if user is None:

        return Response(
            {
                "success": False,
                "message": "Identifiants invalides."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:

        return Response(
            {
                "success": False,
                "message": "Ce compte NSIKAY est désactivé."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    token, created = Token.objects.get_or_create(
        user=user
    )

    return Response(
        {
            "success": True,
            "message": "Connexion NSIKAY réussie.",
            "token": token.key,
            "user": UserSerializer(user).data,
        }
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):

    Token.objects.filter(
        user=request.user
    ).delete()

    return Response(
        {
            "success": True,
            "message": "Déconnexion réussie."
        }
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def me(request):

    user = request.user

    groups = list(
        user.groups.values_list(
            "name",
            flat=True
        )
    )

    return Response(
        {
            "success": True,
            "user": UserSerializer(user).data,
            "permissions": {
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "groups": groups,
            }
        }
    )


# ============================================================
# UTILISATEURS
# ============================================================

@api_view(["GET"])
@permission_classes([AllowAny])
def users(request):

    return Response(
        {
            "module": "API Utilisateurs NSIKAY",
            "profils": User.objects.count(),
            "statuts": [
                "active",
                "verification",
                "bloque"
            ],
            "permissions": "actives"
        }
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):

    return Response(
        {
            "success": True,
            "user": UserSerializer(request.user).data,
        }
    )


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):

    user = request.user

    allowed_fields = [
        "email",
        "first_name",
        "last_name",
    ]

    changed = False

    for field in allowed_fields:

        if field in request.data:

            value = request.data.get(field)

            if field == "email" and value:
                value = value.strip().lower()

            setattr(user, field, value)
            changed = True

    if changed:
        user.save()

    return Response(
        {
            "success": True,
            "message": "Profil NSIKAY mis à jour.",
            "user": UserSerializer(user).data,
        }
    )


# ============================================================
# MODULES EXISTANTS
# ============================================================

@api_view(["GET"])
@permission_classes([AllowAny])
def banks(request):

    return Response(
        {
            "module": "API Banques NSIKAY",
            "activation": True,
            "services": [
                "deposit",
                "withdraw",
                "transfer",
                "wallet"
            ],
            "devises": [
                "CDF",
                "USD",
                "EUR"
            ]
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def countries(request):

    return Response(
        {
            "module": "API Pays NSIKAY",
            "supervision": True,
            "controle": "actif"
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def certifications(request):

    return Response(
        {
            "module": "API Certification NSIKAY",
            "KYC": True,
            "documents": "validation",
            "alertes": True
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def transactions(request):

    return Response(
        {
            "module": "API Transactions NSIKAY",
            "historique": True,
            "transferts": True,
            "controle": True
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def finance(request):

    return Response(
        {
            "module": "API Finance NSIKAY",
            "wallet": True,
            "solde_reel": True,
            "statistiques": True,
            "graphiques": True
        }
    )
