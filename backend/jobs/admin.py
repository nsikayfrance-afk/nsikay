from django.contrib import admin

from .models import (
    Company,
    JobOffer,
    Application,
    Training,
    Opportunity,
    InsurancePartner,
    InsuranceProduct,
    EmploymentInsurance,
    EmploymentEngagement,
    EmploymentContract,
    EmploymentContractAnnex,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "country",
        "city",
        "administrative_status",
        "certification_status",
        "is_active",
    )

    list_filter = (
        "administrative_status",
        "certification_status",
        "country",
        "is_active",
    )

    search_fields = (
        "name",
        "sector",
        "country",
        "city",
        "email",
    )


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company",
        "country",
        "employment_type",
        "status",
        "published_at",
    )

    list_filter = (
        "status",
        "employment_type",
        "country",
        "remote",
    )

    search_fields = (
        "title",
        "company__name",
        "sector",
        "country",
        "city",
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "candidate_name",
        "offer",
        "status",
        "reviewed_by",
        "created_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "candidate_name",
        "candidate_email",
        "offer__title",
        "offer__company__name",
    )


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "organization",
        "status",
        "is_active",
    )

    list_filter = (
        "status",
        "country",
    )

    search_fields = (
        "title",
        "organization",
        "category",
    )


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "organization",
        "status",
        "is_active",
    )

    list_filter = (
        "status",
        "country",
        "category",
    )

    search_fields = (
        "title",
        "organization",
        "category",
    )


@admin.register(InsurancePartner)
class InsurancePartnerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "legal_name",
        "registration_number",
        "country",
        "status",
        "is_active",
        "certification_date",
    )

    list_filter = (
        "status",
        "is_active",
        "country",
    )

    search_fields = (
        "name",
        "legal_name",
        "registration_number",
        "country",
        "email",
        "phone",
    )


@admin.register(InsuranceProduct)
class InsuranceProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "partner",
        "status",
        "duration_months",
        "price",
        "currency",
        "is_active",
    )

    list_filter = (
        "status",
        "is_active",
        "currency",
    )

    search_fields = (
        "name",
        "partner__name",
        "partner__legal_name",
        "coverage",
    )


@admin.register(EmploymentInsurance)
class EmploymentInsuranceAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "job_offer",
        "product",
        "policy_number",
        "status",
        "coverage_start",
        "coverage_end",
    )

    list_filter = (
        "status",
        "product__partner",
    )

    search_fields = (
        "company__name",
        "job_offer__title",
        "product__name",
        "product__partner__name",
        "policy_number",
        "certificate_reference",
    )

# ============================================================
# ENGAGEMENT / CONTRAT / ANNEXES
# ============================================================

@admin.register(EmploymentEngagement)
class EmploymentEngagementAdmin(admin.ModelAdmin):

    list_display = (
        "position_title",
        "application",
        "status",
        "start_date",
        "end_date",
        "validated_by",
    )

    list_filter = (
        "status",
        "salary_currency",
    )

    search_fields = (
        "position_title",
        "application__candidate_name",
        "application__candidate_email",
        "application__offer__title",
        "application__offer__company__name",
    )


@admin.register(EmploymentContract)
class EmploymentContractAdmin(admin.ModelAdmin):

    list_display = (
        "contract_number",
        "title",
        "engagement",
        "status",
        "start_date",
        "end_date",
        "validated_by",
        "worker_accepted_at",
    )

    list_filter = (
        "status",
        "contract_type",
        "salary_currency",
    )

    search_fields = (
        "contract_number",
        "title",
        "engagement__application__candidate_name",
        "engagement__application__candidate_email",
        "engagement__application__offer__company__name",
    )

    readonly_fields = (
        "worker_acceptance_token",
        "worker_accepted_at",
    )


@admin.register(EmploymentContractAnnex)
class EmploymentContractAnnexAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "contract",
        "is_required",
        "status",
        "validated_by",
        "validated_at",
    )

    list_filter = (
        "status",
        "is_required",
    )

    search_fields = (
        "title",
        "contract__contract_number",
        "contract__engagement__application__candidate_name",
    )
