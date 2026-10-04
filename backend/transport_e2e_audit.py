import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from django.contrib.auth import get_user_model
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
from certification.models import NSIKAYCertification
from wenze.models import WenzeOrder

User = get_user_model()

print("")
print("=" * 60)
print(" NSIKAY - E2E TRANSPORT ORM")
print("=" * 60)

# ------------------------------------------------------------
# USERS
# ------------------------------------------------------------

print("")
print("[USERS]")

users = User.objects.filter(is_active=True).order_by("id")

print("TOTAL_USERS=", users.count())

for user in users[:15]:
    print(
        "USER",
        user.id,
        getattr(user, "username", ""),
        "staff=", getattr(user, "is_staff", False),
        "superuser=", getattr(user, "is_superuser", False),
    )

# ------------------------------------------------------------
# CERTIFICATIONS
# ------------------------------------------------------------

print("")
print("[CERTIFICATIONS]")

cert_qs = NSIKAYCertification.objects.all().order_by("-id")

print("TOTAL_CERTIFICATIONS=", cert_qs.count())

for cert in cert_qs[:15]:
    print(
        "CERT",
        cert.id,
        "owner=", cert.owner_id,
        "type=", cert.certification_type,
        "activity=", cert.activity,
        "status=", cert.status,
    )

# ------------------------------------------------------------
# WENZE
# ------------------------------------------------------------

print("")
print("[WENZE]")

orders = WenzeOrder.objects.all().order_by("-id")

print("TOTAL_WENZE_ORDERS=", orders.count())

for order in orders[:15]:
    print(
        "ORDER",
        order.id,
        "reference=", order.reference,
        "buyer=", order.buyer_id,
        "status=", order.status,
        "currency=", order.currency_id,
        "amount=", order.total_amount,
    )

# ------------------------------------------------------------
# TRANSPORT COMPANIES
# ------------------------------------------------------------

print("")
print("[TRANSPORT COMPANIES]")

companies = TransportCompany.objects.select_related(
    "company",
    "certification",
).all().order_by("-id")

print("TOTAL_TRANSPORT_COMPANIES=", companies.count())

for company in companies[:20]:
    cert = company.certification

    print(
        "COMPANY",
        company.id,
        "business_company=", company.company_id,
        "name=", company.company.name,
        "type=", company.transport_type,
        "country=", company.country,
        "city=", company.city,
        "certification_id=", company.certification_id,
        "cert_status=", cert.status if cert else None,
        "cert_required=", company.certification_required,
        "active=", company.active,
        "validated_by_admin=", company.validated_by_admin,
    )

# ------------------------------------------------------------
# VEHICLES
# ------------------------------------------------------------

print("")
print("[VEHICLES]")

vehicles = TransportVehicle.objects.all().order_by("-id")

print("TOTAL_VEHICLES=", vehicles.count())

for vehicle in vehicles[:20]:
    print(
        "VEHICLE",
        vehicle.id,
        "company=", vehicle.transport_company_id,
        "type=", vehicle.vehicle_type,
        "registration=", vehicle.registration_number,
        "status=", vehicle.status,
        "active=", vehicle.active,
    )

# ------------------------------------------------------------
# DRIVERS
# ------------------------------------------------------------

print("")
print("[DRIVERS]")

drivers = TransportDriver.objects.all().order_by("-id")

print("TOTAL_DRIVERS=", drivers.count())

for driver in drivers[:20]:
    print(
        "DRIVER",
        driver.id,
        "company=", driver.transport_company_id,
        "user=", driver.user_id,
        "license=", driver.license_number,
        "active=", driver.active,
        "validated=", driver.validated,
    )

# ------------------------------------------------------------
# SERVICES
# ------------------------------------------------------------

print("")
print("[TRANSPORT SERVICES]")

services = TransportService.objects.select_related(
    "transport_company",
    "currency",
).all().order_by("-id")

print("TOTAL_TRANSPORT_SERVICES=", services.count())

for service in services[:20]:
    print(
        "SERVICE",
        service.id,
        "company=", service.transport_company_id,
        "type=", service.service_type,
        "pricing=", service.pricing_mode,
        "currency=", service.currency_id,
        "active=", service.active,
    )

# ------------------------------------------------------------
# WENZE DELIVERIES
# ------------------------------------------------------------

print("")
print("[WENZE DELIVERIES]")

deliveries = WenzeDelivery.objects.select_related(
    "order",
    "transport_company",
    "vehicle",
    "driver",
).all().order_by("-id")

print("TOTAL_DELIVERIES=", deliveries.count())

for delivery in deliveries[:20]:
    print(
        "DELIVERY",
        delivery.id,
        "order=", delivery.order_id,
        "company=", delivery.transport_company_id,
        "vehicle=", delivery.vehicle_id,
        "driver=", delivery.driver_id,
        "status=", delivery.status,
        "tracking=", delivery.tracking_reference,
    )

# ------------------------------------------------------------
# PASSENGER RIDES
# ------------------------------------------------------------

print("")
print("[PASSENGER RIDES]")

rides = PassengerRide.objects.all().order_by("-id")

print("TOTAL_RIDES=", rides.count())

for ride in rides[:20]:
    print(
        "RIDE",
        ride.id,
        "passenger=", ride.passenger_id,
        "company=", ride.transport_company_id,
        "service=", ride.transport_service_id,
        "vehicle=", ride.vehicle_id,
        "driver=", ride.driver_id,
        "status=", ride.status,
        "reference=", ride.reference,
    )

# ------------------------------------------------------------
# PASSENGER RENTALS
# ------------------------------------------------------------

print("")
print("[PASSENGER RENTALS]")

rentals = PassengerRental.objects.all().order_by("-id")

print("TOTAL_RENTALS=", rentals.count())

for rental in rentals[:20]:
    print(
        "RENTAL",
        rental.id,
        "passenger=", rental.passenger_id,
        "company=", rental.transport_company_id,
        "service=", rental.transport_service_id,
        "vehicle=", rental.vehicle_id,
        "status=", rental.status,
        "reference=", rental.reference,
    )

# ------------------------------------------------------------
# TRACKING
# ------------------------------------------------------------

print("")
print("[TRACKING]")

tracking = TransportTrackingEvent.objects.all()

print("TOTAL_TRACKING_EVENTS=", tracking.count())

# ------------------------------------------------------------
# RELATION WENZE -> TRANSPORT
# ------------------------------------------------------------

print("")
print("[RELATION WENZE -> TRANSPORT]")

for order in orders[:10]:
    delivery = WenzeDelivery.objects.filter(
        order_id=order.id
    ).first()

    if delivery is not None:
        print(
            "ORDER",
            order.reference,
            "=> DELIVERY",
            delivery.tracking_reference,
            "status=",
            delivery.status,
        )
    else:
        print(
            "ORDER",
            order.reference,
            "=> NO_DELIVERY"
        )

# ------------------------------------------------------------
# TEST DE REGLE DE CERTIFICATION
# ------------------------------------------------------------

print("")
print("[CERTIFICATION RULE AUDIT]")

companies_requiring_cert = TransportCompany.objects.filter(
    certification_required=True
)

print(
    "COMPANIES_REQUIRING_CERT=",
    companies_requiring_cert.count()
)

for company in companies_requiring_cert[:20]:

    cert = company.certification

    certified_approved = (
        cert is not None
        and cert.status == "approved"
    )

    activation_valid = (
        not company.certification_required
        or (
            certified_approved
            and company.validated_by_admin
        )
    )

    print(
        "COMPANY",
        company.id,
        "cert_approved=",
        certified_approved,
        "admin_validated=",
        company.validated_by_admin,
        "activation_should_be_allowed=",
        activation_valid,
        "database_active=",
        company.active,
    )

print("")
print("=" * 60)
print(" AUDIT TERMINE")
print("=" * 60)