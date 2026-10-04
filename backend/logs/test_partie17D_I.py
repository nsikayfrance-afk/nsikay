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

from certification.activity_api import (
    ActivityCertificationListView,
    ActivityCertificationDetailView,
    ActivityCertificationHistoryView,
    ActivityCertificationActionView,
)


User = get_user_model()
factory = APIRequestFactory()

normal_user = User.objects.get(
    username="test_wallet_user2"
)

authority_user = User.objects.get(
    username="DORIS"
)

authority_group = Group.objects.get(
    name="Autorité Certification"
)

initial_group_state = set(
    authority_user.groups.values_list(
        "id",
        flat=True
    )
)

print("NORMAL_USER=", normal_user.username)
print("AUTHORITY_USER=", authority_user.username)

try:

    with transaction.atomic():

        profile = NsikayProfile.objects.filter(
            user=normal_user,
            is_primary=True,
            profile_type="person",
        ).first()

        if profile is None:

            profile = NsikayProfile.objects.create(
                user=normal_user,
                profile_type="person",
                display_name="Profil Test 17-D-I",
                is_primary=True,
                certification_required=False,
                certification_status="not_required",
            )

        activity = Activity.objects.create(
            profile=profile,
            name="Activité Test 17-D-I",
            activity_type="professional",
            description="Test transactionnel API certification",
            sector="Test",
            country="CD",
            city="Kinshasa",
            status="draft",
            visibility="public",
            certification_required=True,
            certification_status="pending",
        )

        certification = NSIKAYCertification.objects.create(
            owner=normal_user,
            certification_type="activity",
            activity=activity.name,
            activity_ref=activity,
            status="pending",
        )

        CertificationHistory.objects.create(
            certification=certification,
            old_status="",
            new_status="pending",
            comment="Création test 17-D-I",
        )

        print("ACTIVITY_ID=", activity.id)
        print("CERTIFICATION_ID=", certification.id)

        # ----------------------------------------------------
        # TEST 1 : UTILISATEUR NORMAL -> LISTE
        # ----------------------------------------------------

        request = factory.get(
            "/certification/activity-certifications/"
        )

        force_authenticate(
            request,
            user=normal_user,
        )

        response = (
            ActivityCertificationListView.as_view()
        )(request)

        print(
            "NORMAL_LIST_STATUS=",
            response.status_code
        )

        if response.status_code != 200:
            raise Exception(
                "La consultation utilisateur normal a échoué."
            )

        # ----------------------------------------------------
        # TEST 2 : UTILISATEUR NORMAL -> DETAIL
        # ----------------------------------------------------

        request = factory.get(
            "/certification/activity-certifications/"
            + str(certification.id)
            + "/"
        )

        force_authenticate(
            request,
            user=normal_user,
        )

        response = (
            ActivityCertificationDetailView.as_view()
        )(
            request,
            certification_id=certification.id,
        )

        print(
            "NORMAL_DETAIL_STATUS=",
            response.status_code
        )

        if response.status_code != 200:
            raise Exception(
                "Le détail utilisateur normal a échoué."
            )

        # ----------------------------------------------------
        # TEST 3 : UTILISATEUR NORMAL -> APPROBATION BLOQUEE
        # ----------------------------------------------------

        request = factory.post(
            "/certification/activity-certifications/"
            + str(certification.id)
            + "/approve/",
            {
                "comment": "Tentative utilisateur normal",
            },
            format="json",
        )

        force_authenticate(
            request,
            user=normal_user,
        )

        response = (
            ActivityCertificationActionView.as_view()
        )(
            request,
            certification_id=certification.id,
            action="approve",
        )

        print(
            "NORMAL_APPROVE_STATUS=",
            response.status_code
        )

        if response.status_code != 403:
            raise Exception(
                "ERREUR : un utilisateur normal peut approuver."
            )

        print("NORMAL_APPROVAL_BLOCKED=OK")

        # ----------------------------------------------------
        # TEST 4 : AJOUT TEMPORAIRE AUTORITE
        # ----------------------------------------------------

        authority_user.groups.add(
            authority_group
        )

        print("AUTHORITY_GROUP_TEMPORARY=ADDED")

        # ----------------------------------------------------
        # TEST 5 : AUTORITE -> LISTE
        # ----------------------------------------------------

        request = factory.get(
            "/certification/activity-certifications/"
        )

        force_authenticate(
            request,
            user=authority_user,
        )

        response = (
            ActivityCertificationListView.as_view()
        )(request)

        print(
            "AUTHORITY_LIST_STATUS=",
            response.status_code
        )

        if response.status_code != 200:
            raise Exception(
                "La liste autorité a échoué."
            )

        # ----------------------------------------------------
        # TEST 6 : AUTORITE -> HISTORIQUE
        # ----------------------------------------------------

        request = factory.get(
            "/certification/activity-certifications/"
            + str(certification.id)
            + "/history/"
        )

        force_authenticate(
            request,
            user=authority_user,
        )

        response = (
            ActivityCertificationHistoryView.as_view()
        )(
            request,
            certification_id=certification.id,
        )

        print(
            "AUTHORITY_HISTORY_STATUS=",
            response.status_code
        )

        if response.status_code != 200:
            raise Exception(
                "L'historique autorité a échoué."
            )

        print(
            "HISTORY_INITIAL_COUNT=",
            response.data["count"]
        )

        # ----------------------------------------------------
        # TEST 7 : AUTORITE -> APPROBATION
        # ----------------------------------------------------

        request = factory.post(
            "/certification/activity-certifications/"
            + str(certification.id)
            + "/approve/",
            {
                "comment": "Certification approuvée - test 17-D-I",
            },
            format="json",
        )

        force_authenticate(
            request,
            user=authority_user,
        )

        response = (
            ActivityCertificationActionView.as_view()
        )(
            request,
            certification_id=certification.id,
            action="approve",
        )

        print(
            "AUTHORITY_APPROVE_STATUS=",
            response.status_code
        )

        if response.status_code != 200:
            raise Exception(
                "L'approbation autorité a échoué."
            )

        certification.refresh_from_db()
        activity.refresh_from_db()

        print(
            "CERTIFICATION_STATUS=",
            certification.status
        )

        print(
            "ACTIVITY_CERTIFICATION_STATUS=",
            activity.certification_status
        )

        if certification.status != "approved":
            raise Exception(
                "La certification n'est pas approved."
            )

        if activity.certification_status != "certified":
            raise Exception(
                "L'activité n'est pas certified."
            )

        # ----------------------------------------------------
        # TEST 8 : HISTORIQUE APRES APPROBATION
        # ----------------------------------------------------

        request = factory.get(
            "/certification/activity-certifications/"
            + str(certification.id)
            + "/history/"
        )

        force_authenticate(
            request,
            user=authority_user,
        )

        response = (
            ActivityCertificationHistoryView.as_view()
        )(
            request,
            certification_id=certification.id,
        )

        print(
            "HISTORY_FINAL_COUNT=",
            response.data["count"]
        )

        if response.data["count"] != 2:
            raise Exception(
                "L'historique final attendu est de 2."
            )

        print("API_CERTIFICATION_WORKFLOW=OK")

        raise RuntimeError(
            "ROLLBACK_TEST_17_D_I"
        )

except RuntimeError as exc:

    if str(exc) != "ROLLBACK_TEST_17_D_I":
        raise

    print("ROLLBACK_TEST=OK")

finally:

    authority_user.groups.set(
        Group.objects.filter(
            id__in=initial_group_state
        )
    )

    print("AUTHORITY_GROUP_STATE_RESTORED=OK")
