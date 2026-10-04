from django.core.management.base import BaseCommand
from service_control.models import GlobalService, ServiceRule


class Command(BaseCommand):
    help = "Charge les regles d'activation des services NSIKAY"

    RULES = {

        "Entreprise": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": True,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Ecole": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Universite": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Centre Formation": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Hopital": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Telecom": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Banque": {
            "certification_required": True,
            "partner_bank_required": True,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": True,
        },

        "Assurance": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Immobilier": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Construction": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": True,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Automobile": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Transport": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": True,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Justice": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Emploi": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": True,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "WENZE": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Evenements": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Publicite": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Reseaux Sociaux": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Video": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Audio": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Sport": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": True,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Musique": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Agriculture": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": True,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Tourisme": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Technologie": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Environnement": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": True,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Social": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": True,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },

        "Religion Histoire Culture": {
            "certification_required": True,
            "partner_bank_required": False,
            "health_insurance_required": False,
            "remote_activation_allowed": True,
            "financial_partner_required": False,
        },
    }

    def handle(self, *args, **options):

        created = 0
        updated = 0
        missing = []

        for service_name, data in self.RULES.items():

            try:
                service = GlobalService.objects.get(
                    name=service_name
                )
            except GlobalService.DoesNotExist:
                missing.append(service_name)
                continue

            rule, was_created = ServiceRule.objects.update_or_create(
                service=service,
                defaults={
                    **data,
                    "admin_validation_required": True,
                    "country_authorization_required": True,
                    "active_by_default": False,
                }
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write("")
        self.stdout.write("=== REGLES SERVICES NSIKAY ===")
        self.stdout.write(f"Regles creees : {created}")
        self.stdout.write(f"Regles mises a jour : {updated}")
        self.stdout.write(f"Regles totales : {ServiceRule.objects.count()}")

        if missing:
            self.stdout.write("")
            self.stdout.write("Services manquants :")
            for name in missing:
                self.stdout.write(f" - {name}")
        else:
            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    "Les 28 services disposent de leurs regles."
                )
            )

