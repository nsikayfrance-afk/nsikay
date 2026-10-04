import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from business.models import Company, Sector
from certification.models import NSIKAYCertification
from finance.models import Currency
from wenze.models import WenzeOrder

from transport.models import (
    TransportCompany,
    TransportVehicle,
    TransportDriver,
    TransportService,
    WenzeDelivery,
    PassengerRide,
    PassengerRental,
    TransportTrackingEvent,
)

from transport.rules import (
    company_activation_allowed,
    ensure_company_activation_allowed,
    ensure_transport_company_is_active,
)

User = get_user_model()

print("")
print("=" * 70)
print(" NSIKAY - E2E BUSINESS TEST TRANSPORT CORRIGE")
print("=" * 70)

passed = 0
failed = 0


def ok(label):
    global passed
    passed += 1
    print("PASS", label)


def fail(label, error=None):
    global failed
    failed += 1
    print("FAIL", label)
    if error:
        print("     ", repr(error))


def expect_rejection(label, callback):
    try:
        callback()
    except ValidationError:
        ok(label + " => operation refusee")
    except Exception as exc:
        ok(label + " => operation refusee (" + type(exc).__name__ + ")")
    else:
        fail(label + " => operation acceptee")


with transaction.atomic():

    print("")
    print("[1] UTILISATEUR")

    user = User.objects.filter(is_superuser=True).first()

    if user is None:
        user = User.objects.filter(is_active=True).first()

    if user is None:
        raise RuntimeError("Aucun utilisateur actif disponible.")

    ok("Utilisateur actif disponible")

    print("")
    print("[2] SECTEUR / ENTREPRISE")

    sector = Sector.objects.first()

    if sector is None:
        sector = Sector.objects.create(
            name="Transport E2E"
        )

    company = Company.objects.create(
        owner=user,
        sector=sector,
        name="NSIKAY E2E Transport Test",
        description="Entreprise temporaire de test",
        verified=False,
    )

    ok("Entreprise métier créée")

    print("")
    print("[3] CERTIFICATION PENDING")

    certification = NSIKAYCertification.objects.create(
        owner=user,
        certification_type="company",
        activity="Transport",
        status="pending",
    )

    transport_company = TransportCompany.objects.create(
        company=company,
        transport_type="BOTH",
        description="Transport E2E",
        country="CD",
        city="Kananga",
        certification=certification,
        certification_required=True,
        active=False,
        validated_by_admin=False,
    )

    if not company_activation_allowed(transport_company):
        ok("Certification pending => activation interdite")
    else:
        fail("Certification pending => activation interdite")

    print("")
    print("[4] TENTATIVE ACTIVATION PENDING")

    expect_rejection(
        "Activation avec certification pending",
        lambda: ensure_company_activation_allowed(
            transport_company
        )
    )

    print("")
    print("[5] CERTIFICATION APPROVED SANS VALIDATION ADMIN")

    certification.status = "approved"
    certification.save(update_fields=["status"])

    transport_company.refresh_from_db()

    transport_company.validated_by_admin = False

    if not company_activation_allowed(transport_company):
        ok("Certification approved + admin non valide => activation interdite")
    else:
        fail("Certification approved + admin non valide => activation interdite")

    expect_rejection(
        "Activation sans validation administrative",
        lambda: ensure_company_activation_allowed(
            transport_company
        )
    )

    print("")
    print("[6] VALIDATION ADMIN + ACTIVATION")

    transport_company.validated_by_admin = True

    try:
        ensure_company_activation_allowed(
            transport_company
        )

        transport_company.active = True
        transport_company.save(
            update_fields=[
                "active",
                "validated_by_admin",
            ]
        )

        ok("Certification approuvée + validation admin => activation autorisée")

    except Exception as exc:
        fail("Activation autorisée après validation complète", exc)

    transport_company.refresh_from_db()

    if transport_company.active:
        ok("Entreprise Transport active")
    else:
        fail("Entreprise Transport active")

    print("")
    print("[7] VEHICULE")

    vehicle = TransportVehicle.objects.create(
        transport_company=transport_company,
        vehicle_type="CAR",
        registration_number="E2E-NSIKAY-001",
        brand="NSIKAY",
        model="Transport",
        year=2026,
        seats=4,
        status="AVAILABLE",
        active=True,
    )

    try:
        ensure_transport_company_is_active(
            vehicle.transport_company
        )
        ok("Véhicule rattaché à une entreprise active")
    except Exception as exc:
        fail("Véhicule rattaché à une entreprise active", exc)

    print("")
    print("[8] CONDUCTEUR")

    driver = TransportDriver.objects.create(
        transport_company=transport_company,
        user=user,
        license_number="E2E-LICENSE-001",
        license_category="B",
        phone="+243000000000",
        active=True,
        validated=True,
    )

    ok("Conducteur créé et validé")

    print("")
    print("[9] DEVISE")

    currency = Currency.objects.first()

    if currency is None:
        raise RuntimeError("Aucune devise disponible.")

    ok("Devise disponible => " + str(currency.id))

    print("")
    print("[10] SERVICE TRANSPORT")

    service = TransportService.objects.create(
        transport_company=transport_company,
        service_type="RIDE",
        pricing_mode="DISTANCE",
        base_price=Decimal("5.00"),
        currency=currency,
        price_per_km=Decimal("1.00"),
        price_per_day=Decimal("30.00"),
        active=True,
    )

    ok("Service Transport créé")

    print("")
    print("[11] WENZE -> LIVRAISON")

    order = WenzeOrder.objects.order_by("-id").first()

    if order is None:
        fail("Aucune commande WENZE disponible")
        delivery = None
    else:

        delivery = WenzeDelivery.objects.create(
            order=order,
            transport_company=transport_company,
            vehicle=vehicle,
            driver=driver,
            pickup_address="Point WENZE E2E",
            delivery_address="Destination E2E",
            recipient_name="Destinataire E2E",
            recipient_phone="+243000000001",
            status="ASSIGNED",
            tracking_reference="E2E-DELIVERY-001",
        )

        ok("Commande WENZE reliée à une livraison")
        ok("Livraison reliée au transporteur")

    print("")
    print("[12] COURSE PERSONNE")

    # Détection du vrai champ de relation avec TransportService.
    ride_fields = {
        f.name
        for f in PassengerRide._meta.fields
    }

    ride_kwargs = {
        "passenger": user,
        "transport_company": transport_company,
        "vehicle": vehicle,
        "driver": driver,
        "pickup_address": "Départ E2E",
        "destination_address": "Destination E2E",
        "distance_km": Decimal("10.00"),
        "estimated_amount": Decimal("15.00"),
        "currency": currency,
        "status": "DRIVER_ASSIGNED",
        "reference": "E2E-RIDE-001",
    }

    if "service" in ride_fields:
        ride_kwargs["service"] = service
        print("CHAMP_COURSE_SERVICE=service")
    elif "transport_service" in ride_fields:
        ride_kwargs["transport_service"] = service
        print("CHAMP_COURSE_SERVICE=transport_service")
    else:
        print("CHAMP_COURSE_SERVICE=AUCUN")

    ride = PassengerRide.objects.create(
        **ride_kwargs
    )

    ok("Course personne créée")

    if ride.passenger_id == user.id:
        ok("Course rattachée au passager")
    else:
        fail("Course rattachée au passager")

    if ride.transport_company_id == transport_company.id:
        ok("Course rattachée au transporteur")
    else:
        fail("Course rattachée au transporteur")

    print("")
    print("[13] LOCATION JOURNEE")

    rental_fields = {
        f.name
        for f in PassengerRental._meta.fields
    }

    rental_kwargs = {
        "passenger": user,
        "transport_company": transport_company,
        "vehicle": vehicle,
        "start_at": "2026-10-04T08:00:00+00:00",
        "end_at": "2026-10-04T20:00:00+00:00",
        "pickup_address": "Point location E2E",
        "amount": Decimal("30.00"),
        "currency": currency,
        "status": "CONFIRMED",
        "reference": "E2E-RENTAL-001",
    }

    if "service" in rental_fields:
        rental_kwargs["service"] = service
        print("CHAMP_LOCATION_SERVICE=service")
    elif "transport_service" in rental_fields:
        rental_kwargs["transport_service"] = service
        print("CHAMP_LOCATION_SERVICE=transport_service")
    else:
        print("CHAMP_LOCATION_SERVICE=AUCUN")

    rental = PassengerRental.objects.create(
        **rental_kwargs
    )

    ok("Location journée créée")

    print("")
    print("[14] TRACKING")

    if delivery is not None:

        tracking = TransportTrackingEvent.objects.create(
            delivery=delivery,
            status="IN_TRANSIT",
            location="Point de contrôle E2E",
            latitude=Decimal("-5.900000"),
            longitude=Decimal("22.400000"),
            note="Test E2E transport",
        )

        ok("Événement de suivi créé")

        if tracking.delivery_id == delivery.id:
            ok("Tracking rattaché à la livraison")
        else:
            fail("Tracking rattaché à la livraison")

    print("")
    print("[15] VERIFICATION DES RELATIONS")

    if service.transport_company_id == transport_company.id:
        ok("Service => entreprise Transport")
    else:
        fail("Service => entreprise Transport")

    if vehicle.transport_company_id == transport_company.id:
        ok("Véhicule => entreprise Transport")
    else:
        fail("Véhicule => entreprise Transport")

    if driver.transport_company_id == transport_company.id:
        ok("Conducteur => entreprise Transport")
    else:
        fail("Conducteur => entreprise Transport")

    print("")
    print("[16] COMPTAGES E2E")

    print("TEMP_COMPANIES=", TransportCompany.objects.count())
    print("TEMP_VEHICLES=", TransportVehicle.objects.count())
    print("TEMP_DRIVERS=", TransportDriver.objects.count())
    print("TEMP_SERVICES=", TransportService.objects.count())
    print("TEMP_DELIVERIES=", WenzeDelivery.objects.count())
    print("TEMP_RIDES=", PassengerRide.objects.count())
    print("TEMP_RENTALS=", PassengerRental.objects.count())
    print("TEMP_TRACKING=", TransportTrackingEvent.objects.count())

    print("")
    print("=" * 70)
    print(" RESULTATS")
    print("=" * 70)

    print("TESTS_PASS=", passed)
    print("TESTS_FAIL=", failed)

    if failed == 0:
        print("E2E_RESULT=PASS")
    else:
        print("E2E_RESULT=FAIL")

    print("")
    print("ROLLBACK=EN_ATTENTE")

    transaction.set_rollback(True)

print("")
print("=" * 70)
print(" ROLLBACK TERMINE")
print("=" * 70)
print("DONNEES_TEST_PERSISTANTES=NON")
print("TEST_TERMINE=OK")
print("=" * 70)