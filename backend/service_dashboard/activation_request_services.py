from dataclasses import dataclass
from django.utils import timezone

from service_control.models import (
    GlobalService,
    CountryServiceStatus,
    ServiceActivation,
    ServiceRule,
)

from certification.models import NSIKAYCertification
from administration.models import HealthInsurance
from banking.models import Bank, BankCountry, BankCountryAccess
from partner_finance.models import PartnerApplication, PartnerCertification


@dataclass
class ActivationRequestCheck:
    allowed: bool
    message: str

    certification_checked: bool = False
    health_insurance_checked: bool = False
    bank_partner_checked: bool = False
    financial_partner_checked: bool = False
    country_authorization_checked: bool = False


class ActivationRequestValidator:

    @staticmethod
    def _country_is_operational(country):
        return bool(
            country
            and country.is_primary
            and country.is_operational
        )

    @staticmethod
    def _certification_is_valid(user, service):
        if not user:
            return False

        certifications = NSIKAYCertification.objects.filter(
            owner=user
        )

        valid_statuses = {"approved", "VALIDE"}

        for certification in certifications:
            if certification.status not in valid_statuses:
                continue

            activity = (certification.activity or "").strip().lower()
            service_name = (service.name or "").strip().lower()

            if not activity or not service_name:
                continue

            if (
                activity == service_name
                or service_name in activity
                or activity in service_name
            ):
                return True

        return False

    @staticmethod
    def _health_insurance_is_valid(user, country):
        if not user:
            return False

        today = timezone.localdate()

        policies = HealthInsurance.objects.filter(
            insured_user=user,
            status="validated",
            validated_by_admin=True,
            start_date__lte=today,
            end_date__gte=today,
        )

        country_name = (country.country_name or "").strip().lower()

        for policy in policies:
            policy_country = (policy.country or "").strip().lower()

            if (
                not policy_country
                or policy_country == country_name
            ):
                return True

        return False

    @staticmethod
    def _bank_exists(country):
        country_name = (country.country_name or "").strip()

        banks = Bank.objects.filter(
            country__iexact=country_name,
            certified=True,
            active=True,
        )

        if banks.exists():
            return True

        banks = Bank.objects.filter(
            certified=True,
            active=True,
            bankcountryaccess__country_name__iexact=country_name,
            bankcountryaccess__approved=True,
        )

        if banks.exists():
            return True

        banks = Bank.objects.filter(
            certified=True,
            active=True,
            bankcountry__country__iexact=country_name,
            bankcountry__approved=True,
        )

        return banks.exists()

    @staticmethod
    def _financial_partner_exists():
        partners = PartnerApplication.objects.filter(
            status="approved"
        )

        for partner in partners:
            try:
                certification = partner.partner_certification_relation
            except Exception:
                certification = None

            if certification is None:
                continue

            if not getattr(certification, "identity_verified", False):
                continue

            if not getattr(certification, "documents_verified", False):
                continue

            return True

        return False

    @staticmethod
    def validate(service, country, user):
        result = ActivationRequestCheck(
            allowed=False,
            message="",
        )

        # ----------------------------------------------------
        # Pays
        # ----------------------------------------------------

        if not country:
            result.message = "Pays introuvable."
            return result

        if not country.is_primary:
            result.message = "Le pays n'est pas un pays ISO principal NSIKAY."
            return result

        if not country.is_operational:
            result.message = (
                "Le pays n'est pas actuellement opérationnel "
                "dans la configuration NSIKAY."
            )
            return result

        # ----------------------------------------------------
        # Relation service / pays
        # ----------------------------------------------------

        activation = ServiceActivation.objects.filter(
            service=service,
            country=country,
        ).first()

        if not activation:
            result.message = (
                "La relation service/pays n'existe pas."
            )
            return result

        result.country_authorization_checked = True

        # ----------------------------------------------------
        # Règle service
        # ----------------------------------------------------

        rule = ServiceRule.objects.filter(
            service=service
        ).first()

        if not rule:
            result.message = (
                "Aucune règle de service n'est définie."
            )
            return result

        # ----------------------------------------------------
        # Certification
        # ----------------------------------------------------

        if rule.certification_required:
            if not ActivationRequestValidator._certification_is_valid(
                user,
                service,
            ):
                result.message = (
                    "Certification NSIKAY valide requise pour ce service."
                )
                return result

            result.certification_checked = True

        else:
            result.certification_checked = True

        # ----------------------------------------------------
        # Assurance santé
        # ----------------------------------------------------

        if rule.health_insurance_required:
            if not ActivationRequestValidator._health_insurance_is_valid(
                user,
                country,
            ):
                result.message = (
                    "Une assurance santé valide et validée par "
                    "l'administration est requise."
                )
                return result

            result.health_insurance_checked = True

        else:
            result.health_insurance_checked = True

        # ----------------------------------------------------
        # Banque
        # ----------------------------------------------------

        if rule.partner_bank_required:
            if not ActivationRequestValidator._bank_exists(country):
                result.message = (
                    "Aucun partenaire bancaire certifié et actif "
                    f"n'est valide pour {country.country_name}."
                )
                return result

            result.bank_partner_checked = True

        else:
            result.bank_partner_checked = True

        # ----------------------------------------------------
        # Partenaire financier
        # ----------------------------------------------------

        if rule.financial_partner_required:
            if not ActivationRequestValidator._financial_partner_exists():
                result.message = (
                    "Aucun partenaire financier certifié "
                    "n'est disponible."
                )
                return result

            result.financial_partner_checked = True

        else:
            result.financial_partner_checked = True

        # ----------------------------------------------------
        # Tout est conforme
        # ----------------------------------------------------

        result.allowed = True
        result.message = (
            "Toutes les conditions administratives de la demande "
            "d'activation sont satisfaites."
        )

        return result


class ActivationRequestManager:

    @staticmethod
    def create(service, country, user, reason="", beneficiary_user=None):
        from service_dashboard.models import ServiceActivationRequest

        beneficiary_user = beneficiary_user or user

        existing = ServiceActivationRequest.objects.filter(
            service=service,
            country=country,
            beneficiary_user=beneficiary_user,
            status="pending",
        ).first()

        if existing:
            return existing, False, "Une demande identique est déjà en attente."

        result = ActivationRequestValidator.validate(
            service,
            country,
            beneficiary_user,
        )

        request = ServiceActivationRequest.objects.create(
            service=service,
            country=country,
            requested_by=user,
            beneficiary_user=beneficiary_user,
            status="pending",
            certification_checked=result.certification_checked,
            health_insurance_checked=result.health_insurance_checked,
            bank_partner_checked=result.bank_partner_checked,
            financial_partner_checked=result.financial_partner_checked,
            country_authorization_checked=result.country_authorization_checked,
            admin_validated=False,
            validation_message=result.message,
            rejection_reason="",
        )

        return request, True, result.message

