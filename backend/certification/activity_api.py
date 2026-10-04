from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status as drf_status

from .models import (
    NSIKAYCertification,
    CertificationHistory,
)

from .activity_workflow import (
    approve_activity_certification,
    reject_activity_certification,
    reopen_activity_certification,
    expire_activity_certification,
)


class IsCertificationAuthority(IsAuthenticated):

    def has_permission(self, request, view):

        if not super().has_permission(request, view):
            return False

        user = request.user

        if getattr(user, "is_superuser", False):
            return True

        return user.groups.filter(
            name__in=[
                "Autorité Certification",
                "Super Administrateur",
            ]
        ).exists()


def certification_payload(certification):

    activity = certification.activity_ref

    return {
        "id": certification.id,
        "certification_type": certification.certification_type,
        "activity": certification.activity,
        "activity_id": (
            activity.id
            if activity is not None
            else None
        ),
        "activity_name": (
            activity.name
            if activity is not None
            else None
        ),
        "activity_type": (
            activity.activity_type
            if activity is not None
            else None
        ),
        "owner_id": certification.owner_id,
        "status": certification.status,
        "document_reference": certification.document_reference,
        "created_at": certification.created_at,
        "updated_at": certification.updated_at,
    }


class ActivityCertificationListView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        queryset = (
            NSIKAYCertification.objects
            .filter(
                certification_type="activity"
            )
            .select_related(
                "owner",
                "activity_ref",
            )
            .order_by("-created_at")
        )

        is_authority = (
            request.user.is_superuser
            or request.user.groups.filter(
                name__in=[
                    "Autorité Certification",
                    "Super Administrateur",
                ]
            ).exists()
        )

        if not is_authority:
            queryset = queryset.filter(
                owner=request.user
            )

        data = [
            certification_payload(item)
            for item in queryset
        ]

        return Response({
            "count": len(data),
            "results": data,
        })


class ActivityCertificationDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get_certification(self, request, certification_id):

        certification = get_object_or_404(
            NSIKAYCertification.objects.select_related(
                "owner",
                "activity_ref",
            ),
            id=certification_id,
            certification_type="activity",
        )

        is_authority = (
            request.user.is_superuser
            or request.user.groups.filter(
                name__in=[
                    "Autorité Certification",
                    "Super Administrateur",
                ]
            ).exists()
        )

        if (
            not is_authority
            and certification.owner_id != request.user.id
        ):
            return None

        return certification

    def get(self, request, certification_id):

        certification = self.get_certification(
            request,
            certification_id,
        )

        if certification is None:
            return Response(
                {
                    "detail": (
                        "Cette certification n'est pas accessible "
                        "à cet utilisateur."
                    )
                },
                status=drf_status.HTTP_403_FORBIDDEN,
            )

        return Response(
            certification_payload(certification)
        )


class ActivityCertificationHistoryView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, certification_id):

        certification = get_object_or_404(
            NSIKAYCertification.objects,
            id=certification_id,
            certification_type="activity",
        )

        is_authority = (
            request.user.is_superuser
            or request.user.groups.filter(
                name__in=[
                    "Autorité Certification",
                    "Super Administrateur",
                ]
            ).exists()
        )

        if (
            not is_authority
            and certification.owner_id != request.user.id
        ):
            return Response(
                {
                    "detail": (
                        "Historique non accessible."
                    )
                },
                status=drf_status.HTTP_403_FORBIDDEN,
            )

        history = (
            CertificationHistory.objects
            .filter(
                certification=certification
            )
            .order_by("created_at", "id")
        )

        results = [
            {
                "id": item.id,
                "old_status": item.old_status,
                "new_status": item.new_status,
                "comment": item.comment,
                "created_at": item.created_at,
            }
            for item in history
        ]

        return Response({
            "certification_id": certification.id,
            "count": len(results),
            "results": results,
        })


class ActivityCertificationActionView(APIView):

    permission_classes = [
        IsCertificationAuthority,
    ]

    ACTIONS = {
        "approve": approve_activity_certification,
        "reject": reject_activity_certification,
        "reopen": reopen_activity_certification,
        "expire": expire_activity_certification,
    }

    def post(self, request, certification_id, action):

        action_function = self.ACTIONS.get(action)

        if action_function is None:
            return Response(
                {
                    "detail": (
                        "Action de certification inconnue."
                    ),
                    "allowed_actions": list(
                        self.ACTIONS.keys()
                    ),
                },
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        certification = get_object_or_404(
            NSIKAYCertification.objects.select_related(
                "activity_ref",
                "owner",
            ),
            id=certification_id,
            certification_type="activity",
        )

        comment = request.data.get(
            "comment",
            "",
        )

        try:

            certification = action_function(
                certification=certification,
                comment=comment,
            )

        except Exception as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            "message": (
                f"Action '{action}' exécutée avec succès."
            ),
            "certification": certification_payload(
                certification
            ),
        })
