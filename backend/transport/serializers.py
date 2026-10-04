from rest_framework import serializers

from .models import (
    TransportCompany,
    TransportVehicle,
    TransportDriver,
    TransportService,
    WenzeDelivery,
    PassengerRide,
    PassengerRental,
    TransportTrackingEvent,
)
from .rules import (
    ensure_company_activation_allowed,
    ensure_transport_company_is_active,
)


class TransportCompanySerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
    )

    certification_status = serializers.SerializerMethodField()

    class Meta:
        model = TransportCompany
        fields = "__all__"
        read_only_fields = (
            "active",
            "validated_by_admin",
        )

    def get_certification_status(self, obj):
        if obj.certification is None:
            return None
        return obj.certification.status

    def validate(self, attrs):
        active = attrs.get(
            "active",
            self.instance.active if self.instance else False,
        )

        if active:
            temp = self.instance

            if temp is not None:
                old_values = {}
                for key, value in attrs.items():
                    old_values[key] = getattr(temp, key)
                    setattr(temp, key, value)

                try:
                    ensure_company_activation_allowed(temp)
                finally:
                    for key, value in old_values.items():
                        setattr(temp, key, value)
            else:
                certification = attrs.get("certification")

                if attrs.get("certification_required", True):
                    if certification is None:
                        raise serializers.ValidationError({
                            "certification": (
                                "La certification NSIKAY est obligatoire "
                                "avant activation."
                            )
                        })

                    if certification.status != "approved":
                        raise serializers.ValidationError({
                            "certification": (
                                "La certification NSIKAY doit être approuvée."
                            )
                        })

                    if not attrs.get("validated_by_admin", False):
                        raise serializers.ValidationError({
                            "validated_by_admin": (
                                "La validation administrative est obligatoire."
                            )
                        })

        return attrs


class TransportVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportVehicle
        fields = "__all__"

    def validate_transport_company(self, company):
        ensure_transport_company_is_active(company)
        return company


class TransportDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportDriver
        fields = "__all__"

    def validate_transport_company(self, company):
        ensure_transport_company_is_active(company)
        return company


class TransportServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportService
        fields = "__all__"
        read_only_fields = (
            "active",
        )

    def validate_transport_company(self, company):
        ensure_transport_company_is_active(company)
        return company

    def validate(self, attrs):
        active = attrs.get(
            "active",
            self.instance.active if self.instance else False,
        )

        company = attrs.get(
            "transport_company",
            self.instance.transport_company
            if self.instance else None,
        )

        if active and company is not None:
            ensure_transport_company_is_active(company)

        return attrs


class WenzeDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = WenzeDelivery
        fields = "__all__"

    def validate(self, attrs):
        company = attrs.get(
            "transport_company",
            self.instance.transport_company
            if self.instance else None,
        )

        if company is not None:
            ensure_transport_company_is_active(company)

        return attrs


class PassengerRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerRide
        fields = "__all__"
        read_only_fields = (
            "passenger",
        )

    def validate(self, attrs):
        company = attrs.get(
            "transport_company",
            self.instance.transport_company
            if self.instance else None,
        )

        if company is not None:
            ensure_transport_company_is_active(company)

        return attrs


class PassengerRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerRental
        fields = "__all__"
        read_only_fields = (
            "passenger",
        )

    def validate(self, attrs):
        company = attrs.get(
            "transport_company",
            self.instance.transport_company
            if self.instance else None,
        )

        if company is not None:
            ensure_transport_company_is_active(company)

        return attrs


class TransportTrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportTrackingEvent
        fields = "__all__"

    def validate(self, attrs):
        delivery = attrs.get("delivery")
        ride = attrs.get("ride")
        rental = attrs.get("rental")

        company = None

        if delivery is not None:
            company = delivery.transport_company

        elif ride is not None:
            company = ride.transport_company

        elif rental is not None:
            company = rental.transport_company

        if company is not None:
            ensure_transport_company_is_active(company)

        return attrs