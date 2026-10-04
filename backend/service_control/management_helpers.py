from django.db import transaction

from service_control.models import (
    GlobalService,
    CountryServiceStatus,
    ServiceActivation,
    ServiceRule,
)


def country_service_status(service, country):
    """
    Retourne l'etat administratif d'un service dans un pays.
    Ne verifie pas la certification d'un prestataire.
    """
    activation = ServiceActivation.objects.filter(
        service=service,
        country=country,
    ).first()

    if not activation:
        return {
            "exists": False,
            "active": False,
            "validated_by_admin": False,
            "message": "Relation service/pays inexistante.",
        }

    return {
        "exists": True,
        "active": activation.active,
        "validated_by_admin": activation.validated_by_admin,
        "message": activation.reason or "Aucune observation.",
    }


def activate_country_service(service, country, reason=None):
    """
    Activation ADMINISTRATIVE du service dans un pays.

    Important :
    - ne demande PAS la certification d'un prestataire ;
    - la certification est controlee plus tard lors de l'exercice
      du service par une personne/entreprise/organisation ;
    - les services financiers restent soumis a la verification
      d'un partenaire bancaire/financier valide.
    """

    if not isinstance(service, GlobalService):
        return False, "Service NSIKAY invalide.", None

    if not isinstance(country, CountryServiceStatus):
        return False, "Pays NSIKAY invalide.", None

    activation = ServiceActivation.objects.filter(
        service=service,
        country=country,
    ).first()

    if not activation:
        return False, "La relation service/pays n'existe pas.", None

    try:
        rule = ServiceRule.objects.get(service=service)
    except ServiceRule.DoesNotExist:
        return False, "Aucune regle d'activation definie pour ce service.", activation

    # Controle obligatoire pour les services financiers.
    if rule.partner_bank_required or rule.financial_partner_required:
        from service_control.services import ServiceActivationValidator

        bank_ok, bank_message = ServiceActivationValidator.check_bank(country)

        if not bank_ok:
            return False, bank_message, activation

        if rule.financial_partner_required:
            partner_ok, partner_message = (
                ServiceActivationValidator.check_financial_partner(country)
            )

            if not partner_ok:
                return False, partner_message, activation

    with transaction.atomic():
        activation.active = True
        activation.validated_by_admin = True
        activation.reason = (
            reason
            or "Service active par l'administration NSIKAY "
               "apres verification des conditions pays."
        )
        activation.save(
            update_fields=[
                "active",
                "validated_by_admin",
                "reason",
            ]
        )

    return True, "Service active dans le pays.", activation


def deactivate_country_service(service, country, reason=None):
    """
    Desactivation administrative d'un service dans un pays.
    """

    if not isinstance(service, GlobalService):
        return False, "Service NSIKAY invalide.", None

    if not isinstance(country, CountryServiceStatus):
        return False, "Pays NSIKAY invalide.", None

    activation = ServiceActivation.objects.filter(
        service=service,
        country=country,
    ).first()

    if not activation:
        return False, "La relation service/pays n'existe pas.", None

    with transaction.atomic():
        activation.active = False
        activation.reason = (
            reason
            or "Service desactive par l'administration NSIKAY."
        )
        activation.save(
            update_fields=[
                "active",
                "reason",
            ]
        )

    return True, "Service desactive dans le pays.", activation

