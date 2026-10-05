import json

from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Application,
    EmploymentEngagement,
    EmploymentContract,
    EmploymentContractAnnex,
    EmploymentInsurance,
    InsuranceProduct,
)


User = get_user_model()


def _has_permission(request, permission):
    if not request.user.is_authenticated:
        return False

    return (
        request.user.is_superuser
        or request.user.has_perm(permission)
    )


def _json_body(request):
    try:
        return json.loads(request.body or "{}")
    except Exception:
        return {}


def _validated_application(application_id):
    return (
        Application.objects
        .select_related(
            "offer",
            "offer__company",
        )
        .filter(
            id=application_id,
            status="ACCEPTEE",
            offer__status__in=["VALIDEE", "PUBLIEE"],
            offer__company__is_active=True,
            offer__company__certification_status="CERTIFIEE",
        )
        .first()
    )


@csrf_exempt
def engagements_api(request):

    if request.method == "GET":

        if not _has_permission(
            request,
            "jobs.review_employmentengagement",
        ):
            return JsonResponse(
                {"detail": "Accès administration requis."},
                status=403,
            )

        qs = (
            EmploymentEngagement.objects
            .select_related(
                "application",
                "application__offer",
                "application__offer__company",
            )
        )

        data = []

        for engagement in qs:
            data.append({
                "id": engagement.id,
                "candidate_name": engagement.application.candidate_name,
                "candidate_email": engagement.application.candidate_email,
                "offer_id": engagement.application.offer_id,
                "offer_title": engagement.application.offer.title,
                "company": engagement.application.offer.company.name,
                "position_title": engagement.position_title,
                "status": engagement.status,
                "engagement_date": engagement.engagement_date,
                "start_date": engagement.start_date,
                "end_date": engagement.end_date,
                "work_location": engagement.work_location,
                "salary_amount": (
                    str(engagement.salary_amount)
                    if engagement.salary_amount is not None
                    else None
                ),
                "salary_currency": engagement.salary_currency,
            })

        return JsonResponse(
            {"count": len(data), "results": data}
        )

    if request.method != "POST":
        return JsonResponse(
            {"detail": "Méthode non autorisée."},
            status=405,
        )

    if not _has_permission(
        request,
        "jobs.add_employmentengagement",
    ):
        return JsonResponse(
            {"detail": "Permission de création d'engagement requise."},
            status=403,
        )

    payload = _json_body(request)

    application_id = payload.get("application_id")

    if not application_id:
        return JsonResponse(
            {"detail": "application_id est obligatoire."},
            status=400,
        )

    application = _validated_application(application_id)

    if not application:
        return JsonResponse(
            {
                "detail": (
                    "La candidature doit être ACCEPTÉE et "
                    "l'offre doit être autorisée."
                )
            },
            status=400,
        )

    if EmploymentEngagement.objects.filter(
        application=application
    ).exists():
        return JsonResponse(
            {"detail": "Cette candidature possède déjà un engagement."},
            status=409,
        )

    engagement = EmploymentEngagement.objects.create(
        application=application,
        status="PREPARE",
        position_title=payload.get(
            "position_title",
            application.offer.title,
        ),
        engagement_date=payload.get("engagement_date") or None,
        start_date=payload.get("start_date") or None,
        end_date=payload.get("end_date") or None,
        work_location=payload.get("work_location", ""),
        salary_amount=payload.get("salary_amount") or None,
        salary_currency=payload.get("salary_currency", "EUR"),
        administration_note=payload.get(
            "administration_note",
            "",
        ),
    )

    return JsonResponse(
        {
            "status": "created",
            "id": engagement.id,
            "engagement_status": engagement.status,
        },
        status=201,
    )


@csrf_exempt
def engagement_validation_api(request, engagement_id):

    if request.method != "POST":
        return JsonResponse(
            {"detail": "Méthode non autorisée."},
            status=405,
        )

    if not _has_permission(
        request,
        "jobs.validate_employmentengagement",
    ):
        return JsonResponse(
            {"detail": "Permission de validation requise."},
            status=403,
        )

    payload = _json_body(request)
    action = payload.get("action", "VALIDER")

    engagement = EmploymentEngagement.objects.filter(
        id=engagement_id
    ).first()

    if not engagement:
        return JsonResponse(
            {"detail": "Engagement introuvable."},
            status=404,
        )

    if action == "ANNULER":
        engagement.status = "ANNULE"
        engagement.administration_note = payload.get(
            "administration_note",
            engagement.administration_note,
        )
        engagement.save(
            update_fields=[
                "status",
                "administration_note",
                "updated_at",
            ]
        )

        return JsonResponse(
            {
                "status": "ok",
                "engagement_status": engagement.status,
            }
        )

    if action != "VALIDER":
        return JsonResponse(
            {"detail": "Action inconnue."},
            status=400,
        )

    engagement.status = "ENGAGE"
    engagement.validated_by = request.user
    engagement.validated_at = timezone.now()

    engagement.save(
        update_fields=[
            "status",
            "validated_by",
            "validated_at",
            "updated_at",
        ]
    )

    return JsonResponse(
        {
            "status": "ok",
            "engagement_status": engagement.status,
        }
    )


@csrf_exempt
def contracts_api(request):

    if request.method == "GET":

        if not _has_permission(
            request,
            "jobs.view_employmentcontract",
        ):
            return JsonResponse(
                {"detail": "Accès administration requis."},
                status=403,
            )

        qs = (
            EmploymentContract.objects
            .select_related(
                "engagement",
                "engagement__application",
                "engagement__application__offer",
                "engagement__application__offer__company",
            )
        )

        data = []

        for contract in qs:
            data.append({
                "id": contract.id,
                "contract_number": contract.contract_number,
                "contract_type": contract.contract_type,
                "title": contract.title,
                "status": contract.status,
                "engagement_id": contract.engagement_id,
                "candidate_name": (
                    contract.engagement.application.candidate_name
                ),
                "candidate_email": (
                    contract.engagement.application.candidate_email
                ),
                "company": (
                    contract.engagement.application.offer.company.name
                ),
                "start_date": contract.start_date,
                "end_date": contract.end_date,
                "salary_amount": (
                    str(contract.salary_amount)
                    if contract.salary_amount is not None
                    else None
                ),
                "salary_currency": contract.salary_currency,
                "worker_accepted_at": contract.worker_accepted_at,
            })

        return JsonResponse(
            {"count": len(data), "results": data}
        )

    if request.method != "POST":
        return JsonResponse(
            {"detail": "Méthode non autorisée."},
            status=405,
        )

    if not _has_permission(
        request,
        "jobs.add_employmentcontract",
    ):
        return JsonResponse(
            {"detail": "Permission de création de contrat requise."},
            status=403,
        )

    payload = _json_body(request)
    engagement_id = payload.get("engagement_id")

    if not engagement_id:
        return JsonResponse(
            {"detail": "engagement_id est obligatoire."},
            status=400,
        )

    engagement = EmploymentEngagement.objects.filter(
        id=engagement_id,
        status="ENGAGE",
    ).first()

    if not engagement:
        return JsonResponse(
            {
                "detail": (
                    "Un contrat ne peut être créé que "
                    "pour un engagement confirmé."
                )
            },
            status=400,
        )

    if EmploymentContract.objects.filter(
        engagement=engagement
    ).exists():
        return JsonResponse(
            {"detail": "Cet engagement possède déjà un contrat."},
            status=409,
        )

    contract_number = payload.get("contract_number")

    if not contract_number:
        contract_number = (
            f"NSK-{timezone.now():%Y%m%d%H%M%S}-{engagement.id}"
        )

    if EmploymentContract.objects.filter(
        contract_number=contract_number
    ).exists():
        return JsonResponse(
            {"detail": "Ce numéro de contrat existe déjà."},
            status=409,
        )

    contract = EmploymentContract.objects.create(
        engagement=engagement,
        contract_number=contract_number,
        contract_type=payload.get(
            "contract_type",
            engagement.application.offer.employment_type,
        ),
        title=payload.get(
            "title",
            engagement.position_title,
        ),
        status="BROUILLON",
        start_date=payload.get(
            "start_date"
        ) or engagement.start_date,
        end_date=payload.get(
            "end_date"
        ) or engagement.end_date,
        salary_amount=payload.get(
            "salary_amount"
        ) or engagement.salary_amount,
        salary_currency=payload.get(
            "salary_currency",
            engagement.salary_currency,
        ),
        administration_note=payload.get(
            "administration_note",
            "",
        ),
    )

    return JsonResponse(
        {
            "status": "created",
            "id": contract.id,
            "contract_number": contract.contract_number,
            "contract_status": contract.status,
        },
        status=201,
    )


@csrf_exempt
def contract_validation_api(request, contract_id):

    if request.method != "POST":
        return JsonResponse(
            {"detail": "Méthode non autorisée."},
            status=405,
        )

    if not _has_permission(
        request,
        "jobs.validate_employmentcontract",
    ):
        return JsonResponse(
            {"detail": "Permission de validation requise."},
            status=403,
        )

    payload = _json_body(request)
    action = payload.get("action", "VALIDER")

    contract = (
        EmploymentContract.objects
        .select_related("engagement")
        .filter(id=contract_id)
        .first()
    )

    if not contract:
        return JsonResponse(
            {"detail": "Contrat introuvable."},
            status=404,
        )

    if action != "VALIDER":
        return JsonResponse(
            {"detail": "Action inconnue."},
            status=400,
        )

    required_annexes = contract.annexes.filter(
        is_required=True
    )

    if required_annexes.filter(
        status="REFUSEE"
    ).exists():
        return JsonResponse(
            {
                "detail": (
                    "Le contrat ne peut pas être validé : "
                    "une annexe obligatoire est refusée."
                )
            },
            status=400,
        )

    if required_annexes.exclude(
        status="VALIDEE"
    ).exists():
        return JsonResponse(
            {
                "detail": (
                    "Toutes les annexes obligatoires doivent "
                    "être validées avant le contrat."
                )
            },
            status=400,
        )

    contract.status = "EN_ATTENTE_TRAVAILLEUR"
    contract.validated_by = request.user
    contract.validated_at = timezone.now()

    contract.save(
        update_fields=[
            "status",
            "validated_by",
            "validated_at",
            "updated_at",
        ]
    )

    return JsonResponse(
        {
            "status": "ok",
            "contract_status": contract.status,
        }
    )


@csrf_exempt
def contract_annexes_api(request, contract_id):

    contract = EmploymentContract.objects.filter(
        id=contract_id
    ).first()

    if not contract:
        return JsonResponse(
            {"detail": "Contrat introuvable."},
            status=404,
        )

    if request.method == "GET":

        if not _has_permission(
            request,
            "jobs.view_employmentcontractannex",
        ):
            return JsonResponse(
                {"detail": "Accès administration requis."},
                status=403,
            )

        data = []

        for annex in contract.annexes.all():
            data.append({
                "id": annex.id,
                "title": annex.title,
                "description": annex.description,
                "is_required": annex.is_required,
                "status": annex.status,
                "created_at": annex.created_at,
            })

        return JsonResponse(
            {"count": len(data), "results": data}
        )

    if request.method != "POST":
        return JsonResponse(
            {"detail": "Méthode non autorisée."},
            status=405,
        )

    if not _has_permission(
        request,
        "jobs.add_employmentcontractannex",
    ):
        return JsonResponse(
            {"detail": "Permission de création d'annexe requise."},
            status=403,
        )

    payload = _json_body(request)

    title = payload.get("title")

    if not title:
        return JsonResponse(
            {"detail": "title est obligatoire."},
            status=400,
        )

    annex = EmploymentContractAnnex.objects.create(
        contract=contract,
        title=title,
        description=payload.get(
            "description",
            "",
        ),
        is_required=payload.get(
            "is_required",
            True,
        ),
        status="SOUMISE",
    )

    return JsonResponse(
        {
            "status": "created",
            "id": annex.id,
            "annex_status": annex.status,
        },
        status=201,
    )


@csrf_exempt
def annex_validation_api(request, annex_id):

    if request.method != "POST":
        return JsonResponse(
            {"detail": "Méthode non autorisée."},
            status=405,
        )

    if not _has_permission(
        request,
        "jobs.validate_employmentcontractannex",
    ):
        return JsonResponse(
            {"detail": "Permission de validation requise."},
            status=403,
        )

    payload = _json_body(request)

    annex = EmploymentContractAnnex.objects.filter(
        id=annex_id
    ).first()

    if not annex:
        return JsonResponse(
            {"detail": "Annexe introuvable."},
            status=404,
        )

    action = payload.get("action", "VALIDER")

    if action == "REFUSER":
        annex.status = "REFUSEE"
    elif action == "VALIDER":
        annex.status = "VALIDEE"
        annex.validated_by = request.user
        annex.validated_at = timezone.now()
    else:
        return JsonResponse(
            {"detail": "Action inconnue."},
            status=400,
        )

    annex.administration_note = payload.get(
        "administration_note",
        annex.administration_note,
    )

    annex.save(
        update_fields=[
            "status",
            "validated_by",
            "validated_at",
            "administration_note",
            "updated_at",
        ]
    )

    return JsonResponse(
        {
            "status": "ok",
            "annex_status": annex.status,
        }
    )


@csrf_exempt
def worker_contract_acceptance_api(request, acceptance_token):

    if request.method != "POST":
        return JsonResponse(
            {"detail": "Méthode non autorisée."},
            status=405,
        )

    contract = (
        EmploymentContract.objects
        .select_related(
            "engagement",
            "engagement__application",
        )
        .filter(
            worker_acceptance_token=acceptance_token,
            status="EN_ATTENTE_TRAVAILLEUR",
        )
        .first()
    )

    if not contract:
        return JsonResponse(
            {
                "detail": (
                    "Contrat introuvable ou non disponible "
                    "pour acceptation."
                )
            },
            status=404,
        )

    required_annexes = contract.annexes.filter(
        is_required=True
    )

    if required_annexes.exclude(
        status="VALIDEE"
    ).exists():
        return JsonResponse(
            {
                "detail": (
                    "Les annexes obligatoires doivent être "
                    "validées avant l'acceptation du contrat."
                )
            },
            status=400,
        )

    payload = _json_body(request)

    contract.status = "ACCEPTE_TRAVAILLEUR"
    contract.worker_accepted_at = timezone.now()
    contract.worker_acceptance_note = payload.get(
        "note",
        "",
    )

    contract.save(
        update_fields=[
            "status",
            "worker_accepted_at",
            "worker_acceptance_note",
            "updated_at",
        ]
    )

    engagement = contract.engagement

    engagement.status = "ENGAGE"
    engagement.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    return JsonResponse(
        {
            "status": "accepted",
            "contract_number": contract.contract_number,
            "contract_status": contract.status,
            "engagement_status": engagement.status,
            "worker_accepted_at": contract.worker_accepted_at,
        }
    )