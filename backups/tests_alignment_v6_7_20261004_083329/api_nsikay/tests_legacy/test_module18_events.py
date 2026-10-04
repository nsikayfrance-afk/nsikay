from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

from api_nsikay.models import NsikayEvent, EventParticipant
from finance.models import Currency, Wallet, WalletTransaction


User = get_user_model()


class EventModule18Test(TestCase):

    def setUp(self):

        self.organizer = User.objects.create_user(
            username="event_admin",
            password="test12345"
        )

        self.participant = User.objects.create_user(
            username="event_user",
            password="test12345"
        )

        self.currency = Currency.objects.get_or_create(
            code="EUR",
            defaults={
                "name": "Euro",
                "symbol": "€",
            }
        )[0]

        self.wallet = Wallet.objects.create(
            user=self.participant,
            currency=self.currency,
            balance=Decimal("100.00")
        )


    def test_creation_evenement(self):

        event = NsikayEvent.objects.create(
            organizer=self.organizer,
            title="Conférence Internationale NSIKAY Nantes 2027",
            description="Création emplois, culture et innovation",
            date=timezone.datetime(
                2027,
                1,
                13,
                tzinfo=timezone.UTC
            ),
            location="Nantes France"
        )

        self.assertIsNotNone(event.id)
        self.assertEqual(
            event.title,
            "Conférence Internationale NSIKAY Nantes 2027"
        )


    def test_participant_evenement(self):

        event = NsikayEvent.objects.create(
            organizer=self.organizer,
            title="NSIKAY EVENT TEST",
            description="Test événement",
            date=timezone.datetime(
                2027,
                1,
                13,
                tzinfo=timezone.UTC
            ),
            location="Nantes France"
        )

        participant = EventParticipant.objects.create(
            event=event,
            user=self.participant
        )

        self.assertEqual(
            participant.event.id,
            event.id
        )


    def test_paiement_ticket_evenement(self):

        event = NsikayEvent.objects.create(
            organizer=self.organizer,
            title="NSIKAY PAYMENT TEST",
            description="Test paiement",
            date=timezone.datetime(
                2027,
                1,
                13,
                tzinfo=timezone.UTC
            ),
            location="Nantes France"
        )


        EventParticipant.objects.create(
            event=event,
            user=self.participant
        )


        transaction = WalletTransaction.objects.create(
            wallet=self.wallet,
            amount=Decimal("25.00"),
            transaction_type="event_registration",
            status="completed",
            reference=f"NSIKAY_EVENT_{event.id}"
        )


        self.assertEqual(
            transaction.amount,
            Decimal("25.00")
        )
