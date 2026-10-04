from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from nsikay_profiles.models import NsikayProfile

from ..models import Activity, Service, Project


class ActivitiesApiTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="activities_test_user",
            password="TestPassword123!",
        )

        self.other_user = User.objects.create_user(
            username="activities_other_user",
            password="TestPassword123!",
        )

        self.profile = NsikayProfile.objects.create(
            user=self.user,
            profile_type="company",
            display_name="Entreprise Activités Test",
        )

        self.other_profile = NsikayProfile.objects.create(
            user=self.other_user,
            profile_type="company",
            display_name="Autre Entreprise",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_activity(self):
        response = self.client.post(
            "/api/activities/",
            {
                "profile": self.profile.id,
                "name": "Activité NSIKAY Test",
                "activity_type": "company",
                "sector": "Technologie & Innovation",
                "status": "active",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Activity.objects.filter(
                name="Activité NSIKAY Test"
            ).exists()
        )

    def test_create_service(self):
        activity = Activity.objects.create(
            profile=self.profile,
            name="Activité Service Test",
            activity_type="service",
            status="active",
        )

        response = self.client.post(
            "/api/services/",
            {
                "activity": activity.id,
                "name": "Service NSIKAY",
                "category": "Conseil",
                "price": "100.00",
                "currency": "EUR",
                "status": "active",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Service.objects.filter(
                name="Service NSIKAY"
            ).exists()
        )

    def test_create_project(self):
        activity = Activity.objects.create(
            profile=self.profile,
            name="Activité Projet Test",
            activity_type="technology",
            status="active",
        )

        response = self.client.post(
            "/api/projects/",
            {
                "activity": activity.id,
                "name": "Projet NSIKAY",
                "description": "Projet de validation.",
                "status": "planned",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Project.objects.filter(
                name="Projet NSIKAY"
            ).exists()
        )

    def test_user_cannot_use_other_profile(self):
        response = self.client.post(
            "/api/activities/",
            {
                "profile": self.other_profile.id,
                "name": "Tentative interdite",
                "activity_type": "company",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_user_cannot_create_service_on_other_activity(self):
        activity = Activity.objects.create(
            profile=self.other_profile,
            name="Activité externe service",
            activity_type="service",
        )

        response = self.client.post(
            "/api/services/",
            {
                "activity": activity.id,
                "name": "Service interdit",
                "status": "active",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("activity", response.data)

    def test_user_cannot_create_project_on_other_activity(self):
        activity = Activity.objects.create(
            profile=self.other_profile,
            name="Activité externe projet",
            activity_type="technology",
        )

        response = self.client.post(
            "/api/projects/",
            {
                "activity": activity.id,
                "name": "Projet interdit",
                "status": "planned",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("activity", response.data)

    def test_user_cannot_access_other_activity(self):
        activity = Activity.objects.create(
            profile=self.other_profile,
            name="Activité privée autre utilisateur",
            activity_type="company",
        )

        response = self.client.get(
            f"/api/activities/{activity.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_services_are_scoped_to_user(self):
        activity = Activity.objects.create(
            profile=self.other_profile,
            name="Activité externe",
            activity_type="service",
        )

        Service.objects.create(
            activity=activity,
            name="Service externe",
        )

        response = self.client.get("/api/services/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

