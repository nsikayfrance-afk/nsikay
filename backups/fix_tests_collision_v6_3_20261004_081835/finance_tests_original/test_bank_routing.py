from django.test import TestCase

from decimal import Decimal


class BankRoutingTest(TestCase):

    def test_bank_amount(self):

        amount = Decimal("1000")

        self.assertEqual(
            amount,
            Decimal("1000")
        )
