from django.test import TestCase
from django.urls import reverse


class NsikayApiHealthTest(TestCase):


    def test_api_alive(self):

        response = self.client.get(
            "/api/nsikay/"
        )

        self.assertNotEqual(
            response.status_code,
            500
        )


