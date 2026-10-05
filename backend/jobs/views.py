from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

import json

from .models import (
    Company,
    JobOffer,
    Application,
    Training,
    Opportunity,
    InsurancePartner,
    InsuranceProduct,
    EmploymentInsurance,
)


def company_data(company):
    return {
        "id": company.id,
        "name": company.name,
        "sector": company.sector,
        "country": company.country,
        "city": company.city,
        "description": company.description,
        "website": company.website,
        "email": company.email,
        "phone": company.phone,
        "administrative_status": company.administrative_status,
        "certification_status": company.certification_status,
        "is_verified": company.is_verified,
        "is_active": company.is_active,
    }


def job_data(job):
    return {
        "id": job.id,
        "title": job.title,
        "slug": job.slug,
        "company": company_data(job.company),
        "sector": job.sector,
        "country": job.country,
        "city": job.city,
        "employment_type": job.employment_type,
        "description": job.description,
        "requirements": job.requirements,
        "salary": job.salary,
        "remote": job.remote,
        "status": job.status,
        "published_at": (
            job.published_at.isoformat()
            if job.published_at
            else None
        ),
        "deadline": (
            job.deadline.isoformat()
            if job.deadline
            else None
        ),
    }


def training_data(item):
    return {
        "id": item.id,
        "title": item.title,
        "organization": item.organization,
        "category": item.category,
        "country": item.country,
        "city": item.city,
        "description": item.description,
        "duration": item.duration,
        "mode": item.mode,
        "url": item.url,
        "status": item.status,
        "is_active": item.is_active,
    }


def opportunity_data(item):
    return {
        "id": item.id,
        "title": item.title,
        "category": item.category,
        "country": item.country,
        "city": item.city,
        "organization": item.organization,
        "description": item.description,
        "url": item.url,
        "status": item.status,
        "is_active": item.is_active,
    }


def insurance_partner_data(partner):
    return {
        "id": partner.id,
        "name": partner.name,
        "legal_name": partner.legal_name,
        "registration_number": partner.registration_number,
        "country": partner.country,
        "email": partner.email,
        "phone": partner.phone,
        "website": partner.website,
        "status": partner.status,
        "is_active": partner.is_active,
        "certification_date": (
            partner.certification_date.isoformat()
            if partner.certification_date
            else None
        ),
    }


def insurance_product_data(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "coverage": product.coverage,
        "duration_months": product.duration_months,
        "price": (
            str(product.price)
            if product.price is not None
            else None
        ),
        "currency": product.currency,
        "status": product.status,
        "is_active": product.is_active,
        "partner": insurance_partner_data(product.partner),
    }


def employment_insurance_data(insurance):
    return {
        "id": insurance.id,
        "company_id": insurance.company_id,
        "company": insurance.company.name,
        "job_offer_id": insurance.job_offer_id,
        "job_offer": (
            insurance.job_offer.title
            if insurance.job_offer
            else None
        ),
        "product_id": insurance.product_id,
        "product": insurance.product.name,
        "partner": insurance.product.partner.name,
        "policy_number": insurance.policy_number,
        "certificate_reference": insurance.certificate_reference,
        "coverage_start": (
            insurance.coverage_start.isoformat()
            if insurance.coverage_start
            else None
        ),
        "coverage_end": (
            insurance.coverage_end.isoformat()
            if insurance.coverage_end
            else None
        ),
        "status": insurance.status,
        "administration_note": insurance.administration_note,
        "rejection_reason": insurance.rejection_reason,
    }


def jobs_api(request):

    if request.method != "GET":
        return JsonResponse(
            {"error": "Méthode non autorisée"},
            status=405,
        )

    from django.db.models import Exists, OuterRef, Q

    validated_insurance = EmploymentInsurance.objects.filter(
        job_offer=OuterRef("pk"),
        status="VALIDEE",
    )

    qs = JobOffer.objects.filter(
        status__in=["VALIDEE", "PUBLIEE"],
        company__is_active=True,
        company__certification_status="CERTIFIEE",
    ).filter(
        Exists(validated_insurance)
    ).select_related("company")

    search = request.GET.get("search", "").strip()
    country = request.GET.get("country", "").strip()
    sector = request.GET.get("sector", "").strip()

    if search:
        qs = qs.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(company__name__icontains=search)
            | Q(city__icontains=search)
        )

    if country:
        qs = qs.filter(country__iexact=country)

    if sector:
        qs = qs.filter(sector__iexact=sector)

    return JsonResponse(
        {
            "success": True,
            "count": qs.count(),
            "results": [job_data(x) for x in qs],
        }
    )


def job_detail_api(request, job_id):

    job = get_object_or_404(
        JobOffer.objects.select_related("company"),
        id=job_id,
        status__in=["VALIDEE", "PUBLIEE"],
        company__is_active=True,
        company__certification_status="CERTIFIEE",
    )

    if not EmploymentInsurance.objects.filter(
        job_offer=job,
        status="VALIDEE",
    ).exists():
        return JsonResponse(
            {
                "success": False,
                "error": (
                    "Cette offre ne peut pas être consultée : "
                    "assurance emploi validée obligatoire."
                ),
            },
            status=403,
        )

    return JsonResponse(
        {
            "success": True,
            "job": job_data(job),
        }
    )


def companies_api(request):

    qs = Company.objects.filter(
        is_active=True,
        certification_status="CERTIFIEE",
    )

    return JsonResponse(
        {
            "success": True,
            "count": qs.count(),
            "results": [company_data(x) for x in qs],
        }
    )


def training_api(request):

    qs = Training.objects.filter(
        is_active=True,
        status="VALIDE",
    )

    return JsonResponse(
        {
            "success": True,
            "count": qs.count(),
            "results": [training_data(x) for x in qs],
        }
    )


def opportunities_api(request):

    qs = Opportunity.objects.filter(
        is_active=True,
        status="VALIDE",
    )

    return JsonResponse(
        {
            "success": True,
            "count": qs.count(),
            "results": [opportunity_data(x) for x in qs],
        }
    )


def insurance_partners_api(request):

    if request.method != "GET":
        return JsonResponse(
            {"error": "Méthode non autorisée"},
            status=405,
        )

    qs = InsurancePartner.objects.filter(
        status="CERTIFIE",
        is_active=True,
    ).order_by("name")

    return JsonResponse(
        {
            "success": True,
            "count": qs.count(),
            "results": [
                insurance_partner_data(x)
                for x in qs
            ],
        }
    )


def insurance_products_api(request):

    if request.method != "GET":
        return JsonResponse(
            {"error": "Méthode non autorisée"},
            status=405,
        )

    qs = InsuranceProduct.objects.filter(
        status="VALIDE",
        is_active=True,
        partner__status="CERTIFIE",
        partner__is_active=True,
    ).select_related("partner").order_by("partner__name", "name")

    partner_id = request.GET.get("partner_id", "").strip()

    if partner_id:
        qs = qs.filter(partner_id=partner_id)

    return JsonResponse(
        {
            "success": True,
            "count": qs.count(),
            "results": [
                insurance_product_data(x)
                for x in qs
            ],
        }
    )


@csrf_exempt
def employment_insurance_api(request):
    """
    Gestion des assurances emploi.

    SECURITE :
    - authentification obligatoire ;
    - lecture des dossiers réservée aux utilisateurs disposant
      de la permission jobs.view_employmentinsurance ;
    - création réservée aux utilisateurs disposant de la permission
      jobs.add_employmentinsurance ;
    - les partenaires et produits doivent être certifiés/validés ;
    - une assurance peut être liée à une offre appartenant à la
      même entreprise.
    """

    # ============================================================
    # 1. AUTHENTIFICATION
    # ============================================================

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "error": "AUTHENTICATION_REQUIRED",
                "message": (
                    "Une authentification est obligatoire "
                    "pour accéder aux dossiers d'assurance emploi."
                ),
            },
            status=401,
        )

    # ============================================================
    # 2. LECTURE
    # ============================================================

    if request.method == "GET":

        if not (
            request.user.is_superuser
            or request.user.has_perm(
                "jobs.view_employmentinsurance"
            )
        ):
            return JsonResponse(
                {
                    "success": False,
                    "error": "PERMISSION_DENIED",
                    "message": (
                        "Vous n'avez pas l'autorisation "
                        "de consulter les dossiers d'assurance emploi."
                    ),
                },
                status=403,
            )

        qs = EmploymentInsurance.objects.select_related(
            "company",
            "job_offer",
            "product",
            "product__partner",
        ).order_by("-created_at")

        company_id = request.GET.get(
            "company_id",
            "",
        ).strip()

        job_offer_id = request.GET.get(
            "job_offer_id",
            "",
        ).strip()

        if company_id:
            qs = qs.filter(
                company_id=company_id
            )

        if job_offer_id:
            qs = qs.filter(
                job_offer_id=job_offer_id
            )

        return JsonResponse(
            {
                "success": True,
                "count": qs.count(),
                "results": [
                    employment_insurance_data(x)
                    for x in qs
                ],
            }
        )

    # ============================================================
    # 3. CREATION
    # ============================================================

    if request.method != "POST":
        return JsonResponse(
            {"error": "Méthode non autorisée"},
            status=405,
        )

    if not (
        request.user.is_superuser
        or request.user.has_perm(
            "jobs.add_employmentinsurance"
        )
    ):
        return JsonResponse(
            {
                "success": False,
                "error": "PERMISSION_DENIED",
                "message": (
                    "Vous n'avez pas l'autorisation "
                    "de créer une assurance emploi."
                ),
            },
            status=403,
        )

    # ============================================================
    # 4. JSON
    # ============================================================

    try:
        data = json.loads(
            request.body or "{}"
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "JSON invalide"},
            status=400,
        )

    required = [
        "company_id",
        "product_id",
    ]

    missing = [
        field
        for field in required
        if not data.get(field)
    ]

    if missing:
        return JsonResponse(
            {
                "error": "Champs obligatoires manquants",
                "fields": missing,
            },
            status=400,
        )

    # ============================================================
    # 5. ENTREPRISE CERTIFIEE
    # ============================================================

    company = get_object_or_404(
        Company,
        id=data["company_id"],
        is_active=True,
        certification_status="CERTIFIEE",
    )

    # ============================================================
    # 6. PRODUIT ASSURANCE VALIDE
    # ============================================================

    product = get_object_or_404(
        InsuranceProduct.objects.select_related(
            "partner"
        ),
        id=data["product_id"],
        status="VALIDE",
        is_active=True,
        partner__status="CERTIFIE",
        partner__is_active=True,
    )

    # ============================================================
    # 7. OFFRE EVENTUELLE
    # ============================================================

    job_offer = None

    if data.get("job_offer_id"):

        job_offer = get_object_or_404(
            JobOffer,
            id=data["job_offer_id"],
            company=company,
        )

        # Une assurance destinée à débloquer une offre doit
        # être attachée à cette offre.
        if job_offer.status in ["REFUSEE", "SUSPENDUE", "EXPIREE"]:
            return JsonResponse(
                {
                    "success": False,
                    "error": "INVALID_JOB_OFFER_STATUS",
                    "message": (
                        "Cette offre ne peut pas recevoir "
                        "une nouvelle assurance dans son état actuel."
                    ),
                },
                status=400,
            )

    # ============================================================
    # 8. CREATION
    # ============================================================

    insurance = EmploymentInsurance.objects.create(
        company=company,
        job_offer=job_offer,
        product=product,
        policy_number=data.get(
            "policy_number",
            "",
        ),
        certificate_reference=data.get(
            "certificate_reference",
            "",
        ),
        coverage_start=data.get(
            "coverage_start"
        ) or None,
        coverage_end=data.get(
            "coverage_end"
        ) or None,
        status="SOUSCRIPTION_EN_COURS",
        administration_note=data.get(
            "administration_note",
            "",
        ),
    )

    return JsonResponse(
        {
            "success": True,
            "insurance_id": insurance.id,
            "status": insurance.status,
            "message": (
                "Assurance enregistrée et "
                "envoyée pour vérification administrative."
            ),
        },
        status=201,
    )


@csrf_exempt
def insurance_verification_api(
    request,
    insurance_id,
):
    """
    Validation administrative d'une assurance d'emploi.

    S?curit? :
    - authentification obligatoire ;
    - Super Administrateur autoris? ;
    - permission jobs.approve_employmentinsurance obligatoire ;
    - validation et refus sont des d?cisions administratives ;
    - l'acteur et la date sont enregistr?s ;
    - un refus doit obligatoirement comporter un motif.
    """

    # --------------------------------------------------------
    # 1. M?thode HTTP
    # --------------------------------------------------------
    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "METHOD_NOT_ALLOWED",
                "message": "M?thode non autoris?e."
            },
            status=405,
        )

    # --------------------------------------------------------
    # 2. Authentification obligatoire
    # --------------------------------------------------------
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "error": "AUTHENTICATION_REQUIRED",
                "message": (
                    "Une authentification est obligatoire "
                    "pour valider ou refuser une assurance."
                ),
            },
            status=401,
        )

    # --------------------------------------------------------
    # 3. Permission administrative
    # --------------------------------------------------------
    if not (
        request.user.is_superuser
        or request.user.has_perm(
            "jobs.approve_employmentinsurance"
        )
    ):
        return JsonResponse(
            {
                "success": False,
                "error": "PERMISSION_DENIED",
                "message": (
                    "Vous n'avez pas l'autorisation "
                    "administrative de valider ou refuser "
                    "cette assurance."
                ),
            },
            status=403,
        )

    # --------------------------------------------------------
    # 4. Assurance
    # --------------------------------------------------------
    insurance = get_object_or_404(
        EmploymentInsurance,
        id=insurance_id,
    )

    # --------------------------------------------------------
    # 5. Lecture JSON
    # --------------------------------------------------------
    try:
        data = json.loads(
            request.body or "{}"
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "error": "INVALID_JSON",
                "message": "JSON invalide.",
            },
            status=400,
        )

    # --------------------------------------------------------
    # 6. Action
    # --------------------------------------------------------
    action = str(
        data.get("action", "")
    ).upper().strip()

    # ========================================================
    # VALIDATION
    # ========================================================
    if action == "VALIDER":

        # ----------------------------------------------------
        # V?rifier le produit d'assurance
        # ----------------------------------------------------
        product = insurance.product

        if not product.is_active:
            return JsonResponse(
                {
                    "success": False,
                    "error": "INSURANCE_PRODUCT_INACTIVE",
                    "message": (
                        "Le produit d'assurance s?lectionn? "
                        "n'est plus actif."
                    ),
                },
                status=400,
            )

        if product.status != "VALIDE":
            return JsonResponse(
                {
                    "success": False,
                    "error": "INSURANCE_PRODUCT_NOT_VALIDATED",
                    "message": (
                        "Le produit d'assurance doit ?tre "
                        "valid? par l'Autorit? de Certification."
                    ),
                },
                status=400,
            )

        # ----------------------------------------------------
        # V?rifier le partenaire d'assurance
        # ----------------------------------------------------
        partner = product.partner

        if not partner.is_active:
            return JsonResponse(
                {
                    "success": False,
                    "error": "INSURANCE_PARTNER_INACTIVE",
                    "message": (
                        "Le partenaire d'assurance "
                        "n'est plus actif."
                    ),
                },
                status=400,
            )

        if partner.status != "CERTIFIE":
            return JsonResponse(
                {
                    "success": False,
                    "error": "INSURANCE_PARTNER_NOT_CERTIFIED",
                    "message": (
                        "Le partenaire d'assurance "
                        "n'est pas certifi?."
                    ),
                },
                status=400,
            )

        # ----------------------------------------------------
        # Validation
        # ----------------------------------------------------
        from django.utils import timezone

        now = timezone.now()

        insurance.status = "VALIDEE"

        insurance.administration_note = data.get(
            "administration_note",
            insurance.administration_note,
        )

        insurance.rejection_reason = ""

        insurance.verified_at = now

        # Enregistrement de l'administrateur
        insurance.verified_by = request.user

        insurance.save(
            update_fields=[
                "status",
                "administration_note",
                "rejection_reason",
                "verified_at",
                "verified_by",
                "updated_at",
            ]
        )

        return JsonResponse(
            {
                "success": True,
                "action": "VALIDER",
                "status": insurance.status,
                "message": (
                    "Assurance valid?e par "
                    "l'Administration."
                ),
                "insurance": {
                    "id": insurance.id,
                    "company_id": insurance.company_id,
                    "job_offer_id": insurance.job_offer_id,
                    "product_id": insurance.product_id,
                    "status": insurance.status,
                    "verified_by": request.user.id,
                    "verified_at": (
                        insurance.verified_at.isoformat()
                        if insurance.verified_at
                        else None
                    ),
                },
            },
            status=200,
        )

    # ========================================================
    # REFUS
    # ========================================================
    if action == "REFUSER":

        reason = str(
            data.get(
                "rejection_reason",
                ""
            )
        ).strip()

        # Un refus sans motif est interdit
        if not reason:
            return JsonResponse(
                {
                    "success": False,
                    "error": "REJECTION_REASON_REQUIRED",
                    "message": (
                        "Un motif est obligatoire "
                        "pour refuser une assurance."
                    ),
                },
                status=400,
            )

        from django.utils import timezone

        now = timezone.now()

        insurance.status = "REFUSEE"

        insurance.rejection_reason = reason

        insurance.administration_note = data.get(
            "administration_note",
            insurance.administration_note,
        )

        insurance.verified_at = now

        # Enregistrement de l'administrateur
        insurance.verified_by = request.user

        insurance.save(
            update_fields=[
                "status",
                "rejection_reason",
                "administration_note",
                "verified_at",
                "verified_by",
                "updated_at",
            ]
        )

        return JsonResponse(
            {
                "success": True,
                "action": "REFUSER",
                "status": insurance.status,
                "message": (
                    "Assurance refus?e par "
                    "l'Administration."
                ),
                "insurance": {
                    "id": insurance.id,
                    "company_id": insurance.company_id,
                    "job_offer_id": insurance.job_offer_id,
                    "product_id": insurance.product_id,
                    "status": insurance.status,
                    "verified_by": request.user.id,
                    "verified_at": (
                        insurance.verified_at.isoformat()
                        if insurance.verified_at
                        else None
                    ),
                    "rejection_reason": (
                        insurance.rejection_reason
                    ),
                },
            },
            status=200,
        )

    # --------------------------------------------------------
    # Action inconnue
    # --------------------------------------------------------
    return JsonResponse(
        {
            "success": False,
            "error": "INVALID_ACTION",
            "message": (
                "L'action doit ?tre VALIDER "
                "ou REFUSER."
            ),
        },
        status=400,
    )
@csrf_exempt

def application_api(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Méthode non autorisée"},
            status=405,
        )

    try:
        data = json.loads(
            request.body or "{}"
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "JSON invalide"},
            status=400,
        )

    required = [
        "offer_id",
        "candidate_name",
        "candidate_email",
    ]

    missing = [
        field
        for field in required
        if not data.get(field)
    ]

    if missing:
        return JsonResponse(
            {
                "error": "Champs obligatoires manquants",
                "fields": missing,
            },
            status=400,
        )

    offer = get_object_or_404(
        JobOffer,
        id=data["offer_id"],
        status__in=["VALIDEE", "PUBLIEE"],
        company__is_active=True,
        company__certification_status="CERTIFIEE",
    )

    # ============================================================
    # VERROU MÉTIER :
    # AUCUNE CANDIDATURE SANS ASSURANCE EMPLOI VALIDÉE
    # ============================================================

    validated_insurance = EmploymentInsurance.objects.filter(
        job_offer=offer,
        status="VALIDEE",
    ).exists()

    if not validated_insurance:
        return JsonResponse(
            {
                "success": False,
                "error": (
                    "Candidature impossible : une assurance "
                    "emploi validée est obligatoire avant "
                    "toute candidature."
                ),
            },
            status=403,
        )

    application = Application.objects.create(
        offer=offer,
        candidate_name=data["candidate_name"],
        candidate_email=data["candidate_email"],
        candidate_phone=data.get(
            "candidate_phone",
            "",
        ),
        message=data.get(
            "message",
            "",
        ),
        cv_url=data.get(
            "cv_url",
            "",
        ),
    )

    return JsonResponse(
        {
            "success": True,
            "application_id": application.id,
            "message": (
                "Candidature enregistrée "
                "avec succès."
            ),
        },
        status=201,
    )



