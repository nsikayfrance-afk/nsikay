from django.db import transaction
from django.core.exceptions import ValidationError

from .models import NSIKAYCertification, CertificationHistory


CERTIFICATION_TO_ACTIVITY_STATUS = {
    "pending": "pending",
    "approved": "certified",
    "rejected": "rejected",
    "expired": "expired",
}


def _validate_certification_status(status):
    valid = {
        value
        for value, label in NSIKAYCertification.STATUS_CHOICES
    }

    if status not in valid:
        raise ValidationError(
            {
                "status": (
                    f"Statut de certification invalide : {status}"
                )
            }
        )


@transaction.atomic
def create_activity_certification(
    *,
    activity,
    owner,
    document_reference=None,
):
    """
    Cree la certification centrale d'une activite.

    Une activite ne peut avoir qu'une certification active
    grace au OneToOneField activity_ref.
    """

    if activity is None:
        raise ValidationError(
            {"activity": "Une activité est obligatoire."}
        )

    if owner is None:
        raise ValidationError(
            {"owner": "Le propriétaire est obligatoire."}
        )

    existing = NSIKAYCertification.objects.filter(
        activity_ref=activity
    ).first()

    if existing:
        return existing

    certification = NSIKAYCertification.objects.create(
        owner=owner,
        certification_type="activity",
        activity=activity.name,
        activity_ref=activity,
        document_reference=document_reference,
        status="pending",
    )

    if activity.certification_required:
        activity.certification_status = "pending"

        if activity.status == "active":
            activity.status = "draft"

        activity.save(
            update_fields=[
                "certification_status",
                "status",
                "updated_at",
            ]
        )

    CertificationHistory.objects.create(
        certification=certification,
        old_status="",
        new_status="pending",
        comment="Certification d'activité créée.",
    )

    return certification


@transaction.atomic
def change_activity_certification_status(
    *,
    certification,
    new_status,
    comment="",
):
    """
    Change le statut de certification et synchronise
    automatiquement le statut de l'activité.
    """

    if certification is None:
        raise ValidationError(
            {"certification": "Certification introuvable."}
        )

    _validate_certification_status(new_status)

    activity = certification.activity_ref

    if activity is None:
        raise ValidationError(
            {
                "activity": (
                    "Cette certification n'est pas liée à une activité."
                )
            }
        )

    old_status = certification.status

    if old_status == new_status:
        return certification

    certification.status = new_status
    certification.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    activity_status = CERTIFICATION_TO_ACTIVITY_STATUS.get(
        new_status
    )

    if activity_status:
        activity.certification_status = activity_status

        if new_status != "approved":
            if activity.status == "active":
                activity.status = "draft"

        activity.save(
            update_fields=[
                "certification_status",
                "status",
                "updated_at",
            ]
        )

    CertificationHistory.objects.create(
        certification=certification,
        old_status=old_status,
        new_status=new_status,
        comment=comment or "",
    )

    return certification


@transaction.atomic
def approve_activity_certification(
    *,
    certification,
    comment="Certification approuvée.",
):
    return change_activity_certification_status(
        certification=certification,
        new_status="approved",
        comment=comment,
    )


@transaction.atomic
def reject_activity_certification(
    *,
    certification,
    comment="Certification refusée.",
):
    return change_activity_certification_status(
        certification=certification,
        new_status="rejected",
        comment=comment,
    )


@transaction.atomic
def expire_activity_certification(
    *,
    certification,
    comment="Certification expirée.",
):
    return change_activity_certification_status(
        certification=certification,
        new_status="expired",
        comment=comment,
    )


@transaction.atomic
def reopen_activity_certification(
    *,
    certification,
    comment="Certification remise en attente.",
):
    return change_activity_certification_status(
        certification=certification,
        new_status="pending",
        comment=comment,
    )


def can_activate_activity(activity):
    """
    Une activité nécessitant une certification ne peut être
    activée que si sa certification est approuvée.
    """

    if not activity.certification_required:
        return True

    certification = (
        NSIKAYCertification.objects
        .filter(activity_ref=activity)
        .first()
    )

    if certification is None:
        return False

    return (
        certification.status == "approved"
        and activity.certification_status == "certified"
    )
