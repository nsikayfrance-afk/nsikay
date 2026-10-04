from django.test import TestCase

from finance.services.commission_engine import generate_fee


class FinanceTest(TestCase):

    def test_transfer_fee(self):

        fee = generate_fee(
            100,
            "transfer"
        )

        self.assertEqual(
            fee,
            0.500
        )
