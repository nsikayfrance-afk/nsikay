import logging

from django.http import HttpRequest
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PasswordRecoveryRequest
from .serializers import (
    PasswordRecoveryRequestSerializer,
    PasswordRecoveryResetSerializer,
    PasswordRecoveryVerifySerializer,
)
from .services import (
    create_recovery_request,
    resolve_user,
    reset_password,
    verify_recovery_code,
)


logger = logging.getLogger("nsikay.account_security")


GENERIC_RESPONSE = (
    "Si les informations correspondent à un compte NSIKAY, "
    "un code de récupération sera envoyé au moyen de contact vérifié."
)


def _client_ip(request: HttpRequest):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded:
        return forwarded.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "")


class PasswordRecoveryRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordRecoveryRequestSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"]

        user = resolve_user(identifier)

        # Réponse identique pour éviter l'énumération des comptes.
        if user is None or not user.is_active:
            logger.info(
                "password_recovery_unknown_identifier"
            )

            return Response(
                {
                    "detail": GENERIC_RESPONSE,
                    "status": "accepted",
                },
                status=status.HTTP_200_OK,
            )

        try:
            recovery, _code = create_recovery_request(
                user=user,
                ip_address=_client_ip(request),
                user_agent=request.META.get(
                    "HTTP_USER_AGENT",
                    "",
                ),
            )
        except Exception:
            logger.exception(
                "password_recovery_delivery_error"
            )

            # Ne pas révéler l'état interne au client.
            return Response(
                {
                    "detail": GENERIC_RESPONSE,
                    "status": "accepted",
                },
                status=status.HTTP_200_OK,
            )

        if recovery is None:
            logger.warning(
                "password_recovery_rate_limited user=%s",
                user.pk,
            )

        return Response(
            {
                "detail": GENERIC_RESPONSE,
                "status": "accepted",
            },
            status=status.HTTP_200_OK,
        )


class PasswordRecoveryVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordRecoveryVerifySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        recovery_id = serializer.validated_data[
            "recovery_id"
        ]

        code = serializer.validated_data["code"]

        try:
            recovery = PasswordRecoveryRequest.objects.get(
                pk=recovery_id
            )
        except PasswordRecoveryRequest.DoesNotExist:
            return Response(
                {
                    "detail":
                    "Code invalide ou expiré."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not verify_recovery_code(
            recovery,
            code,
        ):
            logger.warning(
                "password_recovery_code_rejected id=%s",
                recovery_id,
            )

            return Response(
                {
                    "detail":
                    "Code invalide ou expiré."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "detail":
                "Code vérifié. Vous pouvez définir un nouveau mot de passe.",
                "verified": True,
            },
            status=status.HTTP_200_OK,
        )


class PasswordRecoveryResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordRecoveryResetSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        recovery_id = serializer.validated_data[
            "recovery_id"
        ]

        code = serializer.validated_data["code"]

        password = serializer.validated_data[
            "password"
        ]

        try:
            recovery = PasswordRecoveryRequest.objects.get(
                pk=recovery_id
            )
        except PasswordRecoveryRequest.DoesNotExist:
            return Response(
                {
                    "detail":
                    "Demande de récupération invalide."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Le code doit être vérifié une seconde fois
        # au moment critique de la modification.
        if not recovery.is_usable():
            return Response(
                {
                    "detail":
                    "La demande de récupération est expirée ou déjà utilisée."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not verify_recovery_code(
            recovery,
            code,
        ):
            return Response(
                {
                    "detail":
                    "Code invalide ou expiré."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            reset_password(
                recovery,
                password,
            )
        except Exception as exc:
            logger.warning(
                "password_recovery_reset_rejected id=%s",
                recovery_id,
            )

            return Response(
                {
                    "detail": str(exc)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(
            "password_recovery_completed user=%s",
            recovery.user_id,
        )

        return Response(
            {
                "detail":
                "Votre mot de passe a été réinitialisé. "
                "Vous pouvez maintenant vous connecter.",
                "status": "completed",
            },
            status=status.HTTP_200_OK,
        )
