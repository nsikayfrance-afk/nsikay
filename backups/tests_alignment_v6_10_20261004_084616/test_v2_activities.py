from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from nsikay_profiles.models import NsikayProfile

from nsikay_activities.models import Activity, Service, Project


User = get_user_model()


class ActivitiesV2Tests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="activity_v2_user",
            email="activityv2@example.com",
            password="TestPass123!"
        )

        self.other_user = User.objects.create_user(
            username="activity_v2_other",
            email="activityv2other@example.com",
            password="TestPass123!"
        )

        self.profile = NsikayProfile.objects.create(
            user=self.user,
            profile_type="person",
            is_primary=True,
            display_name="Entreprise V2",
        )

        self.other_profile = NsikayProfile.objects.create(
            user=self.other_user,
            profile_type="person",
            is_primary=True,
            display_name="Entreprise Autre",
        )

        self.client.force_authenticate(user=self.user)

    def test_dashboard_empty(self):
        response = self.client.get(
            reverse("activities-dashboard")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profiles"], 0)
        self.assertEqual(response.data["activities"], 0)
        self.assertEqual(response.data["services"], 0)
        self.assertEqual(response.data["projects"], 0)

    def test_create_activity_and_dashboard(self):
        response = self.client.post(
            reverse("activities-list-create"),
            {
                "profile": self.profile.id,
                "name": "Activité V2",
                "activity_type": "professional",
                "description": "Activité professionnelle",
                "sector": "Technologie & Innovation",
                "country": "France",
                "city": "Nantes",
                "status": "active",
                "visibility": "public",
                "certification_required": True,
                "certification_status": "pending",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["profile_display_name"], "Entreprise V2")
        self.assertEqual(response.data["profile_type"], "company")
        self.assertEqual(response.data["service_count"], 0)
        self.assertEqual(response.data["project_count"], 0)

        dashboard = self.client.get(
            reverse("activities-dashboard")
        )

        self.assertEqual(dashboard.status_code, status.HTTP_200_OK)
        self.assertEqual(dashboard.data["activities"], 1)
        self.assertEqual(dashboard.data["activities_active"], 1)
        self.assertEqual(dashboard.data["certification_required"], 1)
        self.assertEqual(dashboard.data["certification_pending"], 1)

    def test_filter_activity_by_search(self):
        Activity.objects.create(
            profile=self.profile,
            name="Plateforme Technologie",
            activity_type="technology",
            status="active",
        )

        Activity.objects.create(
            profile=self.profile,
            name="Service Agriculture",
            activity_type="agriculture",
            status="draft",
        )

        response = self.client.get(
            reverse("activities-list-create"),
            {"q": "Technologie"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["name"],
            "Plateforme Technologie"
        )

    def test_filter_activity_by_status(self):
        Activity.objects.create(
            profile=self.profile,
            name="Active V2",
            activity_type="professional",
            status="active",
        )

        Activity.objects.create(
            profile=self.profile,
            name="Brouillon V2",
            activity_type="professional",
            status="draft",
        )

        response = self.client.get(
            reverse("activities-list-create"),
            {"status": "active"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["name"],
            "Active V2"
        )

    def test_service_and_project_counts(self):
        activity = Activity.objects.create(
            profile=self.profile,
            name="Activité complète",
            activity_type="company",
            status="active",
        )

        Service.objects.create(
            activity=activity,
            name="Service 1",
            price="100.00",
            currency="EUR",
            status="active",
        )

        Service.objects.create(
            activity=activity,
            name="Service 2",
            price="200.00",
            currency="EUR",
            status="draft",
        )

        Project.objects.create(
            activity=activity,
            name="Projet 1",
            status="active",
        )

        response = self.client.get(
            reverse("activity-detail", kwargs={"pk": activity.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["service_count"], 2)
        self.assertEqual(response.data["project_count"], 1)

    def test_cannot_access_other_user_activity(self):
        activity = Activity.objects.create(
            profile=self.other_profile,
            name="Activité privée autre utilisateur",
            activity_type="company",
        )

        response = self.client.get(
            reverse("activity-detail", kwargs={"pk": activity.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_cannot_create_activity_with_other_profile(self):
        response = self.client.post(
            reverse("activities-list-create"),
            {
                "profile": self.other_profile.id,
                "name": "Tentative interdite",
                "activity_type": "professional",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_service_isolation(self):
        activity = Activity.objects.create(
            profile=self.other_profile,
            name="Activité autre",
            activity_type="company",
        )

        service = Service.objects.create(
            activity=activity,
            name="Service autre",
            price="50.00",
            currency="EUR",
        )

        response = self.client.get(
            reverse("service-detail", kwargs={"pk": service.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_project_isolation(self):
        activity = Activity.objects.create(
            profile=self.other_profile,
            name="Projet autre",
            activity_type="company",
        )

        project = Project.objects.create(
            activity=activity,
            name="Projet autre",
        )

        response = self.client.get(
            reverse("project-detail", kwargs={"pk": project.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
