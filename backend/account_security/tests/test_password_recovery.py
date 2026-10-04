from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from account_security.models import PasswordRecoveryRequest
from account_security.services import (
    hash_code,
)


class PasswordRecoveryAPITests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="password_recovery_test",
            email="password.recovery@test.local",
            password="OldPassword123!",
        )

    @patch(
        "account_security.services.send_mail"
    )
    def test_request_is_generic_and_creates_code(
        self,
        send_mail_mock,
    ):
        response = self.client.post(
            "/api/auth/password-recovery/request/",
            {
                "identifier":
                "password.recovery@test.local"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["status"],
            "accepted",
        )

        self.assertEqual(
            PasswordRecoveryRequest.objects.count(),
            1,
        )

        send_mail_mock.assert_called_once()

    def test_unknown_identifier_does_not_enumerate(self):
        response = self.client.post(
            "/api/auth/password-recovery/request/",
            {
                "identifier":
                "unknown-address@test.local"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["status"],
            "accepted",
        )

        self.assertEqual(
            PasswordRecoveryRequest.objects.count(),
            0,
        )

    @patch(
        "account_security.services.send_mail"
    )
    def test_verify_and_reset(
        self,
        send_mail_mock,
    ):
        request, code = (
            self._create_recovery()
        )

        verify = self.client.post(
            "/api/auth/password-recovery/verify/",
            {
                "recovery_id": request.pk,
                "code": code,
            },
            format="json",
        )

        self.assertEqual(
            verify.status_code,
            200,
        )

        reset = self.client.post(
            "/api/auth/password-recovery/reset/",
            {
                "recovery_id": request.pk,
                "code": code,
                "password": "NewPassword456!",
                "password_confirm": "NewPassword456!",
            },
            format="json",
        )

        self.assertEqual(
            reset.status_code,
            200,
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password(
                "NewPassword456!"
            )
        )

        request.refresh_from_db()

        self.assertTrue(
            request.used
        )

    @patch(
        "account_security.services.send_mail"
    )
    def test_expired_code_is_rejected(
        self,
        send_mail_mock,
    ):
        request, code = (
            self._create_recovery()
        )

        request.expires_at = (
            timezone.now()
            - timedelta(minutes=1)
        )

        request.save(
            update_fields=["expires_at"]
        )

        response = self.client.post(
            "/api/auth/password-recovery/verify/",
            {
                "recovery_id": request.pk,
                "code": code,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    @patch(
        "account_security.services.send_mail"
    )
    def test_wrong_code_is_rejected(
        self,
        send_mail_mock,
    ):
        request, _code = (
            self._create_recovery()
        )

        response = self.client.post(
            "/api/auth/password-recovery/verify/",
            {
                "recovery_id": request.pk,
                "code": "000000",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        request.refresh_from_db()

        self.assertEqual(
            request.attempts,
            1,
        )

    def _create_recovery(self):
        from account_security.services import (
            create_recovery_request,
        )

        request, code = create_recovery_request(
            self.user,
            ip_address="127.0.0.1",
            user_agent="NSIKAY-Test",
        )

        self.assertIsNotNone(request)
        self.assertIsNotNone(code)

        return request, code
