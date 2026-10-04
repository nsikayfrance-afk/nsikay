import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction

from nsikay_profiles.models import NsikayProfile
from nsikay_activities.models import Activity

from certification.models import (
    NSIKAYCertification,
    CertificationHistory,
)

from certification.activity_workflow import (
    create_activity_certification,
    approve_activity_certification,
    can_activate_activity,
)

User = get_user_model()

TEST_MARKER = "TEST_17_D_J_3_D"

print("")
print("============================================================")
print(" TEST TRANSACTIONNEL ACTIVITE / CERTIFICATION")
print("============================================================")

user = (
    User.objects
    .filter(
        username="constantkayembedoris",
        is_active=True,
    )
    .first()
)

if user is None:
    raise RuntimeError(
        "Utilisateur principal NSIKAY introuvable."
    )

profile = (
    NsikayProfile.objects
    .filter(
        user=user,
        is_primary=True,
        profile_type="person",
    )
    .first()
)

if profile is None:
    raise RuntimeError(
        "Profil personnel principal introuvable."
    )

print(f"USER_ID={user.id}")
print(f"PROFILE_ID={profile.id}")
print(f"USERNAME={user.username}")

try:

    with transaction.atomic():

        # ----------------------------------------------------
        # 1. CREATION ACTIVITE
        # ----------------------------------------------------

        activity = Activity.objects.create(
            profile=profile,
            name=TEST_MARKER,
            activity_type="professional",
            description="Test transactionnel NSIKAY.",
            sector="Technologie",
            country="CD",
            city="Kananga",
            status="draft",
            visibility="private",
            certification_required=True,
            certification_status="pending",
        )

        print(f"ACTIVITY_ID={activity.id}")
        print(f"STATUS_INITIAL={activity.status}")
        print(
            "CERTIFICATION_STATUS_INITIAL="
            f"{activity.certification_status}"
        )

        # ----------------------------------------------------
        # 2. CREATION PAR LE WORKFLOW CENTRAL
        # ----------------------------------------------------

        certification = create_activity_certification(
            activity=activity,
            owner=user,
            document_reference=TEST_MARKER,
        )

        activity.refresh_from_db()
        certification.refresh_from_db()

        print(
            f"CERTIFICATION_ID={certification.id}"
        )

        print(
            "CERTIFICATION_INITIAL="
            f"{certification.status}"
        )

        history_initial = (
            CertificationHistory.objects
            .filter(
                certification=certification
            )
            .count()
        )

        print(
            f"HISTORY_INITIAL={history_initial}"
        )

        if history_initial != 1:
            raise RuntimeError(
                "Le workflow de création doit créer "
                "une entrée d'historique initiale."
            )

        print(
            "CREATION_CERTIFICATION_WORKFLOW=OK"
        )

        # ----------------------------------------------------
        # 3. ACTIVATION AVANT APPROBATION
        # ----------------------------------------------------

        if can_activate_activity(activity):
            raise RuntimeError(
                "ERREUR : activation autorisée avant approbation."
            )

        print(
            "ACTIVATION_AVANT_APPROBATION_BLOQUEE=OK"
        )

        # ----------------------------------------------------
        # 4. APPROBATION
        # ----------------------------------------------------

        certification = approve_activity_certification(
            certification=certification,
            comment=(
                "Test transactionnel 17-D-J-3-D-C."
            ),
        )

        activity.refresh_from_db()
        certification.refresh_from_db()

        print(
            f"CERTIFICATION_APPROVED="
            f"{certification.status}"
        )

        print(
            "ACTIVITY_CERTIFICATION="
            f"{activity.certification_status}"
        )

        if certification.status != "approved":
            raise RuntimeError(
                "La certification n'est pas approved."
            )

        if activity.certification_status != "certified":
            raise RuntimeError(
                "L'activité n'est pas certified."
            )

        # ----------------------------------------------------
        # 5. ACTIVATION APRES CERTIFICATION
        # ----------------------------------------------------

        if not can_activate_activity(activity):
            raise RuntimeError(
                "L'activation devrait maintenant être autorisée."
            )

        activity.status = "active"

        activity.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        activity.refresh_from_db()

        print(
            f"ACTIVITY_FINAL_STATUS="
            f"{activity.status}"
        )

        if activity.status != "active":
            raise RuntimeError(
                "L'activité n'est pas active."
            )

        # ----------------------------------------------------
        # 6. HISTORIQUE FINAL
        # ----------------------------------------------------

        history_final = (
            CertificationHistory.objects
            .filter(
                certification=certification
            )
            .count()
        )

        print(
            f"HISTORY_FINAL={history_final}"
        )

        if history_final != 2:
            raise RuntimeError(
                "L'historique attendu est : "
                "pending puis approved."
            )

        print(
            "CYCLE_ACTIVITE_CERTIFICATION_ACTIVATION=OK"
        )

        # ----------------------------------------------------
        # 7. ROLLBACK
        # ----------------------------------------------------

        raise RuntimeError(
            "ROLLBACK_TEST_17_D_J_3_D_C"
        )

except RuntimeError as exc:

    if str(exc) == "ROLLBACK_TEST_17_D_J_3_D_C":
        print("ROLLBACK_TEST=OK")
    else:
        raise

# ------------------------------------------------------------
# 8. AUDIT POST-ROLLBACK
# ------------------------------------------------------------

print("")
print("============================================================")
print(" AUDIT POST-ROLLBACK")
print("============================================================")

activities_total = Activity.objects.count()

certifications_total = (
    NSIKAYCertification.objects.count()
)

certifications_activity = (
    NSIKAYCertification.objects
    .filter(
        certification_type="activity"
    )
    .count()
)

histories_total = (
    CertificationHistory.objects.count()
)

activities_with_certification = (
    Activity.objects
    .filter(
        nsikay_certification__isnull=False
    )
    .count()
)

print(
    f"ACTIVITES_TOTAL={activities_total}"
)

print(
    f"CERTIFICATIONS_TOTAL="
    f"{certifications_total}"
)

print(
    "CERTIFICATIONS_TYPE_ACTIVITY="
    f"{certifications_activity}"
)

print(
    f"HISTORIQUES_TOTAL={histories_total}"
)

print(
    "ACTIVITES_AVEC_CERTIFICATION="
    f"{activities_with_certification}"
)

if (
    activities_total != 11
    or certifications_total != 0
    or certifications_activity != 0
    or histories_total != 0
    or activities_with_certification != 0
):
    raise RuntimeError(
        "AUDIT_POST_ROLLBACK_INATTENDU"
    )

print("")
print("AUDIT_POST_ROLLBACK=OK")
print("TEST_17_D_J_3_D_C_TERMINE")
