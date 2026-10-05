from django.urls import path

from .employment_flow import (
    engagements_api,
    engagement_validation_api,
    contracts_api,
    contract_validation_api,
    contract_annexes_api,
    annex_validation_api,
    worker_contract_acceptance_api,
)
from .views import (
    jobs_api,
    job_detail_api,
    companies_api,
    training_api,
    opportunities_api,
    application_api,
    insurance_partners_api,
    insurance_products_api,
    employment_insurance_api,
    insurance_verification_api,
)


urlpatterns = [
    path("", jobs_api),
    path("offers/", jobs_api),
    path("offers/<int:job_id>/", job_detail_api),
    path("companies/", companies_api),
    path("training/", training_api),
    path("opportunities/", opportunities_api),
    path("applications/", application_api),

    # ASSURANCE
    path("insurance/partners/", insurance_partners_api),
    path("insurance/products/", insurance_products_api),
    path(
        "insurance/employment/",
        employment_insurance_api,
    ),
    path(
        "insurance/employment/<int:insurance_id>/verify/",
        insurance_verification_api,
    ),
]

# ============================================================
# ENGAGEMENT / CONTRAT / ANNEXES
# ============================================================

urlpatterns += [
    path(
        "employment/engagements/",
        engagements_api,
    ),
    path(
        "employment/engagements/<int:engagement_id>/validate/",
        engagement_validation_api,
    ),
    path(
        "employment/contracts/",
        contracts_api,
    ),
    path(
        "employment/contracts/<int:contract_id>/validate/",
        contract_validation_api,
    ),
    path(
        "employment/contracts/<int:contract_id>/annexes/",
        contract_annexes_api,
    ),
    path(
        "employment/annexes/<int:annex_id>/validate/",
        annex_validation_api,
    ),
    path(
        "employment/contracts/accept/<uuid:acceptance_token>/",
        worker_contract_acceptance_api,
    ),
]