from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from nsikay_profiles.models import NsikayProfile


User = get_user_model()


class NsikayProfileAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="profile_test_user",
            email="profile@test.nsikay",
            password="TestProfile123!"
        )

        self.client.force_authenticate(user=self.user)

        self.url = "/api/profiles/"

    def test_list_profiles_empty(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(response.data, [])

    def test_create_profile(self):
        payload = {
            "profile_type": "person",
            "display_name": "NSIKAY Test",
            "legal_name": "",
            "professional_title": "Membre NSIKAY",
            "description": "Profil de test NSIKAY",
            "country": "RDC",
            "city": "Kananga",
            "phone": "",
            "website": "",
            "sector": "",
            "visibility": "public",
            "status": "draft",
            "is_primary": True,
            "certification_required": False,
            "certification_status": "not_required",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.data
        )

        profile = NsikayProfile.objects.get(
            user=self.user
        )

        self.assertEqual(
            profile.display_name,
            "NSIKAY Test"
        )

        self.assertEqual(
            profile.profile_type,
            "person"
        )

    def test_update_profile(self):
        profile = NsikayProfile.objects.create(
            user=self.user,
            profile_type="person",
            display_name="Ancien nom",
            status="draft"
        )

        response = self.client.patch(
            f"{self.url}{profile.id}/",
            {
                "display_name": "Nouveau nom",
                "city": "Kananga",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data
        )

        profile.refresh_from_db()

        self.assertEqual(profile.display_name, "Nouveau nom")
        self.assertEqual(profile.city, "Kananga")

    def test_delete_profile(self):
        profile = NsikayProfile.objects.create(
            user=self.user,
            profile_type="person",
            display_name="Profil à supprimer",
            status="draft"
        )

        response = self.client.delete(
            f"{self.url}{profile.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            NsikayProfile.objects.filter(
                id=profile.id
            ).exists()
        )

    def test_user_cannot_access_other_user_profile(self):
        other_user = User.objects.create_user(
            username="other_profile_user",
            email="other@test.nsikay",
            password="TestProfile123!"
        )

        other_profile = NsikayProfile.objects.create(
            user=other_user,
            profile_type="person",
            display_name="Profil autre utilisateur",
            status="draft"
        )

        response = self.client.get(
            f"{self.url}{other_profile.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
