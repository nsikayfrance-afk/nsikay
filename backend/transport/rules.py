from django.core.exceptions import ValidationError


def certification_is_approved(certification):
    """
    Utilise exclusivement NSIKAYCertification existante.
    Aucune certification parallèle n'est créée.
    """
    return (
        certification is not None
        and certification.status == "approved"
    )


def company_activation_allowed(company):
    """
    Une entreprise Transport soumise à certification ne peut
    être active que si :
      1. une certification NSIKAY existe ;
      2. son statut est approved ;
      3. la validation administrative est effectuée.
    """
    if not company.certification_required:
        return True

    return (
        certification_is_approved(company.certification)
        and company.validated_by_admin
    )


def ensure_company_activation_allowed(company):
    if not company.certification_required:
        return

    if company.certification is None:
        raise ValidationError(
            "La certification NSIKAY est obligatoire avant "
            "l'activation de cette entreprise de transport."
        )

    if company.certification.status != "approved":
        raise ValidationError(
            "L'entreprise de transport ne peut pas être activée "
            "tant que sa certification NSIKAY n'est pas approuvée."
        )

    if not company.validated_by_admin:
        raise ValidationError(
            "La validation administrative NSIKAY est obligatoire "
            "avant l'activation de cette entreprise de transport."
        )


def ensure_transport_company_is_active(company):
    if not company.active:
        raise ValidationError(
            "L'entreprise de transport n'est pas active."
        )

    ensure_company_activation_allowed(company)