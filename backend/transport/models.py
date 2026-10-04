from decimal import Decimal

from django.conf import settings
from django.db import models


class TransportCompany(models.Model):

    TRANSPORT_TYPE_CHOICES = (
        ("GOODS", "Transport de marchandises"),
        ("PASSENGER", "Transport de personnes"),
        ("BOTH", "Marchandises et personnes"),
    )

    company = models.OneToOneField(
        "business.Company",
        on_delete=models.CASCADE,
        related_name="transport_profile",
    )

    transport_type = models.CharField(
        max_length=20,
        choices=TRANSPORT_TYPE_CHOICES,
        default="BOTH",
    )

    description = models.TextField(blank=True)

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    email = models.EmailField(blank=True)

    website = models.URLField(blank=True)

    country = models.CharField(
        max_length=100,
    )

    city = models.CharField(
        max_length=100,
    )

    certification = models.ForeignKey(
        "certification.NSIKAYCertification",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transport_companies",
    )

    certification_required = models.BooleanField(
        default=True,
    )

    active = models.BooleanField(
        default=False,
    )

    validated_by_admin = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["company__name"]

    def __str__(self):
        return self.company.name


class TransportVehicle(models.Model):

    VEHICLE_TYPE_CHOICES = (
        ("CAR", "Voiture"),
        ("TAXI", "Taxi"),
        ("MOTORCYCLE", "Moto"),
        ("VAN", "Minibus / Van"),
        ("BUS", "Bus"),
        ("TRUCK", "Camion"),
        ("PICKUP", "Pick-up"),
        ("TRAILER", "Remorque"),
        ("OTHER", "Autre"),
    )

    STATUS_CHOICES = (
        ("AVAILABLE", "Disponible"),
        ("BUSY", "En service"),
        ("MAINTENANCE", "Maintenance"),
        ("INACTIVE", "Inactif"),
    )

    transport_company = models.ForeignKey(
        TransportCompany,
        on_delete=models.CASCADE,
        related_name="vehicles",
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES,
    )

    registration_number = models.CharField(
        max_length=50,
        unique=True,
    )

    brand = models.CharField(
        max_length=100,
        blank=True,
    )

    model = models.CharField(
        max_length=100,
        blank=True,
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    seats = models.PositiveIntegerField(
        default=1,
    )

    cargo_capacity_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE",
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.registration_number} - {self.vehicle_type}"


class TransportDriver(models.Model):

    transport_company = models.ForeignKey(
        TransportCompany,
        on_delete=models.CASCADE,
        related_name="drivers",
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transport_driver",
    )

    license_number = models.CharField(
        max_length=100,
        unique=True,
    )

    license_category = models.CharField(
        max_length=100,
        blank=True,
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    validated = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.user} - {self.license_number}"


class TransportService(models.Model):

    SERVICE_TYPE_CHOICES = (
        ("GOODS_DELIVERY", "Livraison de marchandises"),
        ("RIDE", "Course / trajet"),
        ("DAILY_RENTAL", "Location à la journée"),
        ("INTERCITY", "Transport interurbain"),
        ("OTHER", "Autre"),
    )

    PRICING_MODE_CHOICES = (
        ("FIXED", "Prix fixe"),
        ("DISTANCE", "Selon distance"),
        ("TIME", "Selon durée"),
        ("QUOTE", "Sur devis"),
    )

    transport_company = models.ForeignKey(
        TransportCompany,
        on_delete=models.CASCADE,
        related_name="services",
    )

    name = models.CharField(
        max_length=255,
    )

    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_TYPE_CHOICES,
    )

    description = models.TextField(blank=True)

    pricing_mode = models.CharField(
        max_length=20,
        choices=PRICING_MODE_CHOICES,
        default="FIXED",
    )

    base_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT,
        related_name="transport_services",
    )

    price_per_km = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    price_per_day = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.transport_company} - {self.name}"


class WenzeDelivery(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "En attente"),
        ("ASSIGNED", "Transporteur assigné"),
        ("PICKED_UP", "Colis récupéré"),
        ("IN_TRANSIT", "En transit"),
        ("DELIVERED", "Livré"),
        ("CANCELLED", "Annulé"),
    )

    order = models.OneToOneField(
        "wenze.WenzeOrder",
        on_delete=models.CASCADE,
        related_name="transport_delivery",
    )

    transport_company = models.ForeignKey(
        TransportCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wenze_deliveries",
    )

    vehicle = models.ForeignKey(
        TransportVehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wenze_deliveries",
    )

    driver = models.ForeignKey(
        TransportDriver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wenze_deliveries",
    )

    pickup_address = models.TextField(blank=True)

    delivery_address = models.TextField(blank=True)

    recipient_name = models.CharField(
        max_length=255,
        blank=True,
    )

    recipient_phone = models.CharField(
        max_length=50,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    tracking_reference = models.CharField(
        max_length=100,
        unique=True,
    )

    requested_at = models.DateTimeField(
        auto_now_add=True,
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.tracking_reference


class PassengerRide(models.Model):

    STATUS_CHOICES = (
        ("REQUESTED", "Demandée"),
        ("ACCEPTED", "Acceptée"),
        ("DRIVER_ASSIGNED", "Conducteur assigné"),
        ("IN_PROGRESS", "En cours"),
        ("COMPLETED", "Terminée"),
        ("CANCELLED", "Annulée"),
    )

    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="passenger_rides",
    )

    transport_company = models.ForeignKey(
        TransportCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="passenger_rides",
    )

    service = models.ForeignKey(
        TransportService,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rides",
    )

    vehicle = models.ForeignKey(
        TransportVehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="passenger_rides",
    )

    driver = models.ForeignKey(
        TransportDriver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="passenger_rides",
    )

    pickup_address = models.TextField()

    destination_address = models.TextField()

    requested_at = models.DateTimeField(
        auto_now_add=True,
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    distance_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    estimated_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT,
        related_name="passenger_rides",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="REQUESTED",
    )

    reference = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.reference


class PassengerRental(models.Model):

    STATUS_CHOICES = (
        ("REQUESTED", "Demandée"),
        ("CONFIRMED", "Confirmée"),
        ("ACTIVE", "En cours"),
        ("COMPLETED", "Terminée"),
        ("CANCELLED", "Annulée"),
    )

    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="passenger_rentals",
    )

    transport_company = models.ForeignKey(
        TransportCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="passenger_rentals",
    )

    service = models.ForeignKey(
        TransportService,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rentals",
    )

    vehicle = models.ForeignKey(
        TransportVehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="passenger_rentals",
    )

    start_at = models.DateTimeField()

    end_at = models.DateTimeField()

    pickup_address = models.TextField(blank=True)

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT,
        related_name="passenger_rentals",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="REQUESTED",
    )

    reference = models.CharField(
        max_length=100,
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.reference


class TransportTrackingEvent(models.Model):

    delivery = models.ForeignKey(
        WenzeDelivery,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tracking_events",
    )

    ride = models.ForeignKey(
        PassengerRide,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tracking_events",
    )

    rental = models.ForeignKey(
        PassengerRental,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tracking_events",
    )

    status = models.CharField(max_length=50)

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
    )

    note = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.status} - {self.created_at}"