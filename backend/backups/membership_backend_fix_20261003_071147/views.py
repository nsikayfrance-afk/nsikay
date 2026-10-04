from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.response import Response

from .models import (
    Member,
    MembershipType,
    MembershipApplication,
    MemberCard,
    Subscription,
    MembershipAuditLog,
)
from .serializers import (
    MembershipTypeSerializer,
    MembershipApplicationSerializer,
    MemberSerializer,
    MemberCardSerializer,
)


def _member_payload(user):
    member = (
        Member.objects
        .filter(user=user)
        .select_related("membership_type")
        .first()
    )

    applications = MembershipApplication.objects.filter(
        user=user
    ).select_related("membership_type")

    if not member:
        return {
            "member": None,
            "applications": MembershipApplicationSerializer(
                applications,
                many=True,
            ).data,
            "card": None,
        }

    card = getattr(member, "official_card", None)

    return {
        "member": MemberSerializer(member).data,
        "applications": MembershipApplicationSerializer(
            applications,
            many=True,
        ).data,
        "card": (
            MemberCardSerializer(card).data
            if card
            else None
        ),
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def membership_types(request):

    items = MembershipType.objects.all().order_by("id")

    return Response(
        MembershipTypeSerializer(
            items,
            many=True,
        ).data
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def membership_me(request):

    return Response(
        _member_payload(request.user)
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def membership_apply(request):

    membership_type_id = request.data.get(
        "membership_type"
    )

    if not membership_type_id:
        return Response(
            {
                "detail": (
                    "Le type d'adhésion est obligatoire."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    membership_type = get_object_or_404(
        MembershipType,
        pk=membership_type_id,
    )

    existing = MembershipApplication.objects.filter(
        user=request.user,
        status__in=[
            "pending",
            "approved_pending_payment",
            "approved",
        ],
    ).first()

    if existing:
        return Response(
            MembershipApplicationSerializer(
                existing
            ).data,
            status=status.HTTP_200_OK,
        )

    with transaction.atomic():

        member, created = Member.objects.get_or_create(
            user=request.user,
            defaults={
                "membership_type": membership_type,
                "status": "pending",
            },
        )

        if member.membership_type_id != membership_type.id:
            member.membership_type = membership_type
            member.status = "pending"
            member.save(
                update_fields=[
                    "membership_type",
                    "status",
                ]
            )

        application = MembershipApplication.objects.create(
            user=request.user,
            membership_type=membership_type,
            message=request.data.get("message", ""),
        )

        MembershipAuditLog.objects.create(
            user=request.user,
            member=member,
            action="APPLICATION_CREATED",
            reference=f"APPLICATION-{application.pk}",
            details={
                "membership_type": membership_type.name,
            },
        )

    return Response(
        _member_payload(request.user),
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def membership_card(request):

    member = get_object_or_404(
        Member,
        user=request.user,
        status="active",
    )

    card = get_object_or_404(
        MemberCard,
        member=member,
    )

    return Response(
        MemberCardSerializer(card).data
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def membership_verify(request, token):

    card = get_object_or_404(
        MemberCard.objects.select_related(
            "member",
            "member__user",
            "member__membership_type",
        ),
        qr_token=token,
    )

    member = card.member
    user = member.user

    return Response(
        {
            "valid": (
                card.status == "active"
                and member.status == "active"
            ),
            "member_number": card.member_number,
            "status": card.status,
            "membership_status": member.status,
            "membership_type": (
                member.membership_type.name
                if member.membership_type
                else None
            ),
            "member_name": (
                user.get_full_name()
                or user.username
            ),
            "issued_at": card.issued_at,
            "expires_at": card.expires_at,
            "organization": {
                "name": "NSIKAY",
                "legal_form": (
                    "Association déclarée en France — loi 1901"
                ),
                "rna": "W442031317",
                "siren": "995 089 711",
                "siret": "995 089 711 00015",
            },
        }
    )


@api_view(["GET"])
@permission_classes([IsAdminUser])
def membership_applications(request):

    applications = (
        MembershipApplication.objects
        .select_related(
            "user",
            "membership_type",
            "reviewed_by",
        )
        .all()
    )

    return Response(
        MembershipApplicationSerializer(
            applications,
            many=True,
        ).data
    )


@api_view(["POST"])
@permission_classes([IsAdminUser])
def membership_review(request, application_id):

    application = get_object_or_404(
        MembershipApplication,
        pk=application_id,
    )

    action = request.data.get("action")

    if action not in [
        "approve",
        "refuse",
        "activate",
    ]:
        return Response(
            {
                "detail": (
                    "Action attendue : "
                    "approve, refuse ou activate."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    member = get_object_or_404(
        Member,
        user=application.user,
    )

    with transaction.atomic():

        if action == "refuse":

            application.status = "refused"
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()

            member.status = "suspended"
            member.save(update_fields=["status"])

            MembershipAuditLog.objects.create(
                user=application.user,
                member=member,
                action="REFUSED",
                reference=f"APPLICATION-{application.pk}",
            )

        elif action == "approve":

            required = (
                application.membership_type
                .contribution_required
            )

            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()

            if required and required > 0:

                application.status = (
                    "approved_pending_payment"
                )

                member.status = "pending"

            else:

                application.status = "approved"
                member.status = "active"

            member.membership_type = (
                application.membership_type
            )

            member.save(
                update_fields=[
                    "membership_type",
                    "status",
                ]
            )

            application.save()

            MembershipAuditLog.objects.create(
                user=application.user,
                member=member,
                action="APPROVED",
                reference=f"APPLICATION-{application.pk}",
                details={
                    "contribution_required": str(required),
                },
            )

            if member.status == "active":

                card, created = MemberCard.objects.get_or_create(
                    member=member
                )

                if created:
                    MembershipAuditLog.objects.create(
                        user=application.user,
                        member=member,
                        action="CARD_CREATED",
                        reference=card.member_number,
                    )

        elif action == "activate":

            required = (
                application.membership_type
                .contribution_required
            )

            if required and required > 0:

                paid = Subscription.objects.filter(
                    member=member,
                    payment_status="paid",
                    amount__gte=required,
                ).exists()

                if not paid:
                    return Response(
                        {
                            "detail": (
                                "La cotisation requise "
                                "n'est pas encore enregistrée "
                                "comme payée."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            member.status = "active"
            member.membership_type = (
                application.membership_type
            )
            member.save(
                update_fields=[
                    "status",
                    "membership_type",
                ]
            )

            application.status = "approved"
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()

            card, created = MemberCard.objects.get_or_create(
                member=member
            )

            MembershipAuditLog.objects.create(
                user=application.user,
                member=member,
                action="ACTIVATED",
                reference=card.member_number,
            )

            if created:
                MembershipAuditLog.objects.create(
                    user=application.user,
                    member=member,
                    action="CARD_CREATED",
                    reference=card.member_number,
                )

    return Response(
        _member_payload(application.user)
    )
