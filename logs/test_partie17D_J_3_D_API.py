import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction

from rest_framework.test import APIRequestFactory, force_authenticate

from nsikay_profiles.models import NsikayProfile
from nsikay_activities.models import Activity

from certification.models import (
    NSIKAYCertification,
    CertificationHistory,
)

from certification.activity_workflow import (
    create_activity_certification,
)

from certification.activity_api import (
    ActivityCertificationListView,
    ActivityCertificationDetailView,
    ActivityCertificationHistoryView,
    ActivityCertificationActionView,
)

User = get_user_model()

TEST_MARKER = "TEST_17_D_J_3_D_API"

factory = APIRequestFactory()

print("")
print("============================================================")
print(" TEST API CERTIFICATION ACTIVITE")
print("============================================================")

normal_user = (
    User.objects
    .filter(
        username="test_wallet_user2",
        is_active=True,
    )
    .first()
)

if normal_user is None:
    raise RuntimeError(
        "Utilisateur normal test_wallet_user2 introuvable."
    )

authority_user = (
    User.objects
    .filter(
        username="DORIS",
        is_active=True,
    )
    .first()
)

if authority_user is None:
    raise RuntimeError(
        "Utilisateur DORIS introuvable."
    )

authority_group = (
    Group.objects
    .filter(
        name="Autorité Certification"
    )
    .first()
)

if authority_group is None:
    raise RuntimeError(
        "Le groupe 'Autorité Certification' "
        "est introuvable."
    )

print(
    f"NORMAL_USER_ID={normal_user.id}"
)

print(
    f"AUTHORITY_USER_ID={authority_user.id}"
)

print(
    f"AUTHORITY_GROUP_ID={authority_group.id}"
)

print(
    "DORIS_GROUPS_BEFORE="
    f"{authority_user.groups.count()}"
)

try:

    with transaction.atomic():

        # ----------------------------------------------------
        # 1. AJOUT TEMPORAIRE DE DORIS A L'AUTORITE
        # ----------------------------------------------------

        authority_group.user_set.add(
            authority_user
        )

        print(
            "AUTHORITY_GROUP_TEMPORARY=ADDED"
        )

        if not authority_user.groups.filter(
            id=authority_group.id
        ).exists():
            raise RuntimeError(
                "DORIS n'a pas été ajouté "
                "au groupe Autorité Certification."
            )

        print(
            "AUTHORITY_PERMISSION_CONTEXT=OK"
        )

        # ----------------------------------------------------
        # 2. PROFIL TEMPORAIRE
        # ----------------------------------------------------

        profile = NsikayProfile.objects.create(
            user=normal_user,
            profile_type="person",
            display_name=TEST_MARKER,
            description="Profil temporaire test API.",
            country="CD",
            city="Kananga",
            visibility="private",
            status="active",
            is_primary=True,
            certification_required=False,
            certification_status="not_required",
        )

        print(
            f"TEMP_PROFILE_ID={profile.id}"
        )

        # ----------------------------------------------------
        # 3. ACTIVITE TEMPORAIRE
        # ----------------------------------------------------

        activity = Activity.objects.create(
            profile=profile,
            name=TEST_MARKER,
            activity_type="professional",
            description="Activité temporaire test API.",
            sector="Technologie",
            country="CD",
            city="Kananga",
            status="draft",
            visibility="private",
            certification_required=True,
            certification_status="pending",
        )

        print(
            f"ACTIVITY_ID={activity.id}"
        )

        # ----------------------------------------------------
        # 4. CERTIFICATION PAR WORKFLOW CENTRAL
        # ----------------------------------------------------

        certification = create_activity_certification(
            activity=activity,
            owner=normal_user,
            document_reference=TEST_MARKER,
        )

        certification.refresh_from_db()

        certification_id = certification.id

        print(
            f"CERTIFICATION_ID={certification_id}"
        )

        print(
            "CERTIFICATION_INITIAL="
            f"{certification.status}"
        )

        # ----------------------------------------------------
        # 5. LISTE UTILISATEUR NORMAL
        # ----------------------------------------------------

        request = factory.get(
            "/certification/activity-certifications/"
        )

        force_authenticate(
            request,
            user=normal_user,
        )

        response = (
            ActivityCertificationListView
            .as_view()
        )(request)

        if response.status_code != 200:
            raise RuntimeError(
                "Liste utilisateur normal incorrecte : "
                f"HTTP {response.status_code}."
            )

        print(
            "NORMAL_LIST_HTTP_200=OK"
        )

        # ----------------------------------------------------
        # 6. DETAIL UTILISATEUR NORMAL
        # ----------------------------------------------------

        request = factory.get(
            f"/certification/activity-certifications/"
            f"{certification_id}/"
        )

        force_authenticate(
            request,
            user=normal_user,
        )

        response = (
            ActivityCertificationDetailView
            .as_view()
        )(
            request,
            certification_id=certification_id,
        )

        if response.status_code != 200:
            raise RuntimeError(
                "Détail utilisateur normal incorrect : "
                f"HTTP {response.status_code}."
            )

        print(
            "NORMAL_DETAIL_HTTP_200=OK"
        )

        # ----------------------------------------------------
        # 7. HISTORIQUE UTILISATEUR NORMAL
        # ----------------------------------------------------

        request = factory.get(
            f"/certification/activity-certifications/"
            f"{certification_id}/history/"
        )

        force_authenticate(
            request,
            user=normal_user,
        )

        response = (
            ActivityCertificationHistoryView
            .as_view()
        )(
            request,
            certification_id=certification_id,
        )

        if response.status_code != 200:
            raise RuntimeError(
                "Historique utilisateur normal incorrect : "
                f"HTTP {response.status_code}."
            )

        print(
            "NORMAL_HISTORY_HTTP_200=OK"
        )

        # ----------------------------------------------------
        # 8. APPROBATION INTERDITE UTILISATEUR NORMAL
        # ----------------------------------------------------

        request = factory.post(
            f"/certification/activity-certifications/"
            f"{certification_id}/approve/",
            {
                "comment": "Tentative utilisateur normal."
            },
            format="json",
        )

        force_authenticate(
            request,
            user=normal_user,
        )

        response = (
            ActivityCertificationActionView
            .as_view()
        )(
            request,
            certification_id=certification_id,
            action="approve",
        )

        if response.status_code != 403:
            raise RuntimeError(
                "L'utilisateur normal a obtenu une "
                "autorisation inattendue : "
                f"HTTP {response.status_code}."
            )

        print(
            "NORMAL_APPROVE_HTTP_403=OK"
        )

        # ----------------------------------------------------
        # 9. LISTE AUTORITE
        # ----------------------------------------------------

        request = factory.get(
            "/certification/activity-certifications/"
        )

        force_authenticate(
            request,
            user=authority_user,
        )

        response = (
            ActivityCertificationListView
            .as_view()
        )(request)

        if response.status_code != 200:
            raise RuntimeError(
                "Liste autorité incorrecte : "
                f"HTTP {response.status_code}."
            )

        print(
            "AUTHORITY_LIST_HTTP_200=OK"
        )

        # ----------------------------------------------------
        # 10. HISTORIQUE AUTORITE
        # ----------------------------------------------------

        request = factory.get(
            f"/certification/activity-certifications/"
            f"{certification_id}/history/"
        )

        force_authenticate(
            request,
            user=authority_user,
        )

        response = (
            ActivityCertificationHistoryView
            .as_view()
        )(
            request,
            certification_id=certification_id,
        )

        if response.status_code != 200:
            raise RuntimeError(
                "Historique autorité incorrect : "
                f"HTTP {response.status_code}."
            )

        print(
            "AUTHORITY_HISTORY_HTTP_200=OK"
        )

        # ----------------------------------------------------
        # 11. APPROBATION PAR AUTORITE
        # ----------------------------------------------------

        request = factory.post(
            f"/certification/activity-certifications/"
            f"{certification_id}/approve/",
            {
                "comment": (
                    "Approbation API test 17-D-J-3-D-B."
                )
            },
            format="json",
        )

        force_authenticate(
            request,
            user=authority_user,
        )

        response = (
            ActivityCertificationActionView
            .as_view()
        )(
            request,
            certification_id=certification_id,
            action="approve",
        )

        if response.status_code != 200:
            raise RuntimeError(
                "Approbation autorité incorrecte : "
                f"HTTP {response.status_code}."
            )

        print(
            "AUTHORITY_APPROVE_HTTP_200=OK"
        )

        # ----------------------------------------------------
        # 12. ETAT FINAL
        # ----------------------------------------------------

        certification.refresh_from_db()
        activity.refresh_from_db()

        print(
            "CERTIFICATION_FINAL="
            f"{certification.status}"
        )

        print(
            "ACTIVITY_CERTIFICATION_FINAL="
            f"{activity.certification_status}"
        )

        if certification.status != "approved":
            raise RuntimeError(
                "Certification finale incorrecte."
            )

        if activity.certification_status != "certified":
            raise RuntimeError(
                "Certification activité incorrecte."
            )

        history_count = (
            CertificationHistory.objects
            .filter(
                certification=certification
            )
            .count()
        )

        print(
            f"HISTORY_FINAL={history_count}"
        )

        if history_count != 2:
            raise RuntimeError(
                "Historique API incorrect."
            )

        print(
            "API_CERTIFICATION_WORKFLOW=OK"
        )

        # ----------------------------------------------------
        # 13. ROLLBACK
        # ----------------------------------------------------

        raise RuntimeError(
            "ROLLBACK_TEST_17_D_J_3_D_API"
        )

except RuntimeError as exc:

    if str(exc) == "ROLLBACK_TEST_17_D_J_3_D_API":
        print(
            "ROLLBACK_TEST=OK"
        )
    else:
        raise

# ------------------------------------------------------------
# 14. AUDIT POST-ROLLBACK
# ------------------------------------------------------------

print("")
print("============================================================")
print(" AUDIT POST-ROLLBACK API")
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

temporary_profiles = (
    NsikayProfile.objects
    .filter(
        display_name=TEST_MARKER
    )
    .count()
)

activities_with_certification = (
    Activity.objects
    .filter(
        nsikay_certification__isnull=False
    )
    .count()
)

doris_groups_after = (
    authority_user.groups.count()
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
    f"TEMP_PROFILES_TOTAL={temporary_profiles}"
)

print(
    "ACTIVITES_AVEC_CERTIFICATION="
    f"{activities_with_certification}"
)

print(
    f"DORIS_GROUPS_AFTER={doris_groups_after}"
)

if (
    activities_total != 11
    or certifications_total != 0
    or certifications_activity != 0
    or histories_total != 0
    or temporary_profiles != 0
    or activities_with_certification != 0
):
    raise RuntimeError(
        "AUDIT_POST_ROLLBACK_API_INATTENDU"
    )

print("")
print("AUDIT_POST_ROLLBACK_API=OK")
print("TEST_17_D_J_3_D_API_TERMINE")
