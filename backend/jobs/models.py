import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Company(models.Model):

    STATUS_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("SOUMISE", "Soumise"),
        ("EN_VERIFICATION", "En vérification"),
        ("VALIDEE", "Validée"),
        ("SUSPENDUE", "Suspendue"),
        ("REFUSEE", "Refusée"),
    ]

    CERTIFICATION_CHOICES = [
        ("NON_CERTIFIEE", "Non certifiée"),
        ("EN_ATTENTE", "Certification en attente"),
        ("CERTIFIEE", "Certifiée"),
        ("SUSPENDUE", "Certification suspendue"),
    ]

    name = models.CharField(max_length=255)

    sector = models.CharField(
        max_length=150,
        blank=True
    )

    country = models.CharField(
        max_length=120,
        blank=True
    )

    city = models.CharField(
        max_length=120,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    # ----------------------------------------------
    # ADMINISTRATION
    # ----------------------------------------------

    administrative_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="BROUILLON"
    )

    certification_status = models.CharField(
        max_length=30,
        choices=CERTIFICATION_CHOICES,
        default="NON_CERTIFIEE"
    )

    is_verified = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=False
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    validated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    suspended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_employment_companies"
    )

    administration_note = models.TextField(
        blank=True
    )

    rejection_reason = models.TextField(
        blank=True
    )

    suspension_reason = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"

    def __str__(self):
        return self.name


class JobOffer(models.Model):

    EMPLOYMENT_TYPES = [
        ("CDI", "CDI"),
        ("CDD", "CDD"),
        ("MISSION", "Mission"),
        ("STAGE", "Stage"),
        ("ALTERNANCE", "Alternance"),
        ("FREELANCE", "Freelance"),
        ("TEMPS_PARTIEL", "Temps partiel"),
    ]

    STATUS_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("SOUMISE", "Soumise"),
        ("EN_VERIFICATION", "En vérification"),
        ("VALIDEE", "Validée"),
        ("PUBLIEE", "Publiée"),
        ("SUSPENDUE", "Suspendue"),
        ("REFUSEE", "Refusée"),
        ("EXPIREE", "Expirée"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="job_offers"
    )

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True
    )

    sector = models.CharField(
        max_length=150,
        blank=True
    )

    country = models.CharField(
        max_length=120,
        blank=True
    )

    city = models.CharField(
        max_length=120,
        blank=True
    )

    employment_type = models.CharField(
        max_length=30,
        choices=EMPLOYMENT_TYPES,
        default="CDI"
    )

    description = models.TextField()

    requirements = models.TextField(
        blank=True
    )

    salary = models.CharField(
        max_length=150,
        blank=True
    )

    remote = models.BooleanField(
        default=False
    )

    # ----------------------------------------------
    # WORKFLOW ADMINISTRATIF
    # ----------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="BROUILLON"
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    validated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True
    )

    suspended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_job_offers"
    )

    administration_note = models.TextField(
        blank=True
    )

    rejection_reason = models.TextField(
        blank=True
    )

    suspension_reason = models.TextField(
        blank=True
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Offre d'emploi"
        verbose_name_plural = "Offres d'emploi"

    def save(self, *args, **kwargs):

        # ==========================================================
        # VERROU ADMINISTRATIF — ASSURANCE EMPLOI OBLIGATOIRE
        # ==========================================================
        #
        # Une offre ne peut devenir VALIDEE ou PUBLIEE que si une
        # assurance emploi liée à cette offre est déjà VALIDEE.
        #
        # Les statuts préparatoires restent autorisés :
        # BROUILLON / SOUMISE / EN_VERIFICATION
        #
        # Les statuts de décision administrative restent possibles :
        # SUSPENDUE / REFUSEE / EXPIREE
        #
        # Ce contrôle protège également les modifications effectuées
        # directement depuis Django Admin ou par du code interne.
        # ==========================================================

        if self.status in ["VALIDEE", "PUBLIEE"] and self.pk:

            assurance_validee = EmploymentInsurance.objects.filter(
                job_offer=self,
                status="VALIDEE",
            ).exists()

            if not assurance_validee:
                from django.core.exceptions import ValidationError

                raise ValidationError(
                    {
                        "status": (
                            "Cette offre ne peut pas être "
                            "validée ou publiée sans une "
                            "assurance emploi VALIDEE liée "
                            "à cette offre."
                        )
                    }
                )

        # ==========================================================
        # GENERATION AUTOMATIQUE DU SLUG
        # ==========================================================

        if not self.slug:
            base = slugify(self.title)
            slug = base
            counter = 2

            while JobOffer.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():

                slug = f"{base}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Application(models.Model):

    STATUS_CHOICES = [
        ("RECUE", "Reçue"),
        ("EN_ETUDE", "En étude"),
        ("SELECTION", "Sélection"),
        ("ENTRETIEN", "Entretien"),
        ("ACCEPTEE", "Acceptée"),
        ("REFUSEE", "Refusée"),
    ]

    offer = models.ForeignKey(
        JobOffer,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    candidate_name = models.CharField(
        max_length=255
    )

    candidate_email = models.EmailField()

    candidate_phone = models.CharField(
        max_length=50,
        blank=True
    )

    message = models.TextField(
        blank=True
    )

    cv_url = models.URLField(
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="RECUE"
    )

    administration_note = models.TextField(
        blank=True
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_employment_applications"
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"

    def __str__(self):
        return f"{self.candidate_name} - {self.offer.title}"


class Training(models.Model):

    STATUS_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("SOUMISE", "Soumise"),
        ("VALIDEE", "Validée"),
        ("PUBLIEE", "Publiée"),
        ("SUSPENDUE", "Suspendue"),
    ]

    title = models.CharField(
        max_length=255
    )

    organization = models.CharField(
        max_length=255,
        blank=True
    )

    category = models.CharField(
        max_length=150,
        blank=True
    )

    country = models.CharField(
        max_length=120,
        blank=True
    )

    city = models.CharField(
        max_length=120,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    duration = models.CharField(
        max_length=100,
        blank=True
    )

    mode = models.CharField(
        max_length=100,
        blank=True
    )

    url = models.URLField(
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="BROUILLON"
    )

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_employment_trainings"
    )

    validated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Opportunity(models.Model):

    STATUS_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("SOUMISE", "Soumise"),
        ("VALIDEE", "Validée"),
        ("PUBLIEE", "Publiée"),
        ("SUSPENDUE", "Suspendue"),
    ]

    title = models.CharField(
        max_length=255
    )

    category = models.CharField(
        max_length=150,
        blank=True
    )

    country = models.CharField(
        max_length=120,
        blank=True
    )

    city = models.CharField(
        max_length=120,
        blank=True
    )

    organization = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    url = models.URLField(
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="BROUILLON"
    )

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_employment_opportunities"
    )

    validated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title





# ============================================================
# ASSURANCE EMPLOI - PARTENAIRES NSIKAY
# ============================================================

class InsurancePartner(models.Model):
    STATUS_CHOICES = [
        ("EN_ATTENTE", "En attente"),
        ("EN_VERIFICATION", "En vérification"),
        ("CERTIFIE", "Certifié"),
        ("SUSPENDU", "Suspendu"),
        ("REFUSE", "Refusé"),
    ]

    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    registration_number = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=80, blank=True)
    website = models.URLField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="EN_ATTENTE",
    )

    is_active = models.BooleanField(default=False)
    certification_date = models.DateTimeField(null=True, blank=True)

    administration_note = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    suspension_reason = models.TextField(blank=True)

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="validated_insurance_partners",
    )
    validated_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Partenaire assurance"
        verbose_name_plural = "Partenaires assurance"
        permissions = [
            ("review_insurancepartner", "Examiner un assureur partenaire"),
            ("certify_insurancepartner", "Certifier un assureur partenaire"),
            ("suspend_insurancepartner", "Suspendre un assureur partenaire"),
        ]

    def __str__(self):
        return self.name


class InsuranceProduct(models.Model):
    STATUS_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("SOUMIS", "Soumis"),
        ("VALIDE", "Validé"),
        ("SUSPENDU", "Suspendu"),
        ("EXPIRE", "Expiré"),
    ]

    partner = models.ForeignKey(
        InsurancePartner,
        on_delete=models.PROTECT,
        related_name="products",
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    coverage = models.TextField(
        help_text="Description de la couverture proposée."
    )

    duration_months = models.PositiveIntegerField(default=12)

    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )

    currency = models.CharField(max_length=10, default="EUR")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="BROUILLON",
    )

    is_active = models.BooleanField(default=False)

    administration_note = models.TextField(blank=True)

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="validated_insurance_products",
    )
    validated_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["partner__name", "name"]
        verbose_name = "Produit assurance"
        verbose_name_plural = "Produits assurance"
        permissions = [
            ("validate_insuranceproduct", "Valider un produit d'assurance"),
            ("suspend_insuranceproduct", "Suspendre un produit d'assurance"),
        ]

    def __str__(self):
        return f"{self.partner.name} - {self.name}"


class EmploymentInsurance(models.Model):
    STATUS_CHOICES = [
        ("SELECTIONNEE", "Sélectionnée"),
        ("SOUSCRIPTION_EN_COURS", "Souscription en cours"),
        ("SOUSCRITE", "Souscrite"),
        ("EN_VERIFICATION", "En vérification"),
        ("VALIDEE", "Validée"),
        ("REFUSEE", "Refusée"),
        ("EXPIREE", "Expirée"),
        ("SUSPENDUE", "Suspendue"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="employment_insurances",
    )

    job_offer = models.ForeignKey(
        JobOffer,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="employment_insurances",
    )

    product = models.ForeignKey(
        InsuranceProduct,
        on_delete=models.PROTECT,
        related_name="employment_insurances",
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="SELECTIONNEE",
    )

    policy_number = models.CharField(max_length=150, blank=True)
    certificate_reference = models.CharField(max_length=150, blank=True)

    coverage_start = models.DateField(null=True, blank=True)
    coverage_end = models.DateField(null=True, blank=True)

    proof_document = models.FileField(
        upload_to="jobs/insurance/",
        null=True,
        blank=True,
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_employment_insurances",
    )

    verified_at = models.DateTimeField(null=True, blank=True)
    administration_note = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Assurance emploi"
        verbose_name_plural = "Assurances emploi"
        permissions = [
            ("verify_employmentinsurance", "Vérifier une assurance emploi"),
            ("approve_employmentinsurance", "Valider une assurance emploi"),
        ]

    def __str__(self):
        return f"{self.company} - {self.product}"

# ============================================================
# EMPLOI - ENGAGEMENT / CONTRAT / ANNEXES
# ============================================================

class EmploymentEngagement(models.Model):

    STATUS_CHOICES = [
        ("PREPARE", "Préparé"),
        ("EN_ATTENTE_CONTRAT", "En attente du contrat"),
        ("ENGAGE", "Engagement confirmé"),
        ("TERMINE", "Terminé"),
        ("ANNULE", "Annulé"),
    ]

    application = models.OneToOneField(
        Application,
        on_delete=models.PROTECT,
        related_name="employment_engagement",
    )

    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default="PREPARE",
    )

    position_title = models.CharField(
        max_length=255,
    )

    engagement_date = models.DateField(
        null=True,
        blank=True,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    work_location = models.CharField(
        max_length=255,
        blank=True,
    )

    salary_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )

    salary_currency = models.CharField(
        max_length=10,
        default="EUR",
    )

    administration_note = models.TextField(
        blank=True,
    )

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_employment_engagements",
    )

    validated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Engagement"
        verbose_name_plural = "Engagements"
        permissions = [
            (
                "review_employmentengagement",
                "Examiner un engagement professionnel",
            ),
            (
                "validate_employmentengagement",
                "Valider un engagement professionnel",
            ),
            (
                "cancel_employmentengagement",
                "Annuler un engagement professionnel",
            ),
        ]

    def __str__(self):
        return f"{self.application.candidate_name} - {self.position_title}"


class EmploymentContract(models.Model):

    STATUS_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("SOUMIS", "Soumis"),
        ("VALIDE", "Validé"),
        ("EN_ATTENTE_TRAVAILLEUR", "En attente du travailleur"),
        ("ACCEPTE_TRAVAILLEUR", "Accepté par le travailleur"),
        ("REFUSE_TRAVAILLEUR", "Refusé par le travailleur"),
        ("TERMINE", "Terminé"),
        ("ANNULE", "Annulé"),
    ]

    engagement = models.OneToOneField(
        EmploymentEngagement,
        on_delete=models.PROTECT,
        related_name="employment_contract",
    )

    contract_number = models.CharField(
        max_length=100,
        unique=True,
    )

    contract_type = models.CharField(
        max_length=50,
    )

    title = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default="BROUILLON",
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    salary_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )

    salary_currency = models.CharField(
        max_length=10,
        default="EUR",
    )

    document = models.FileField(
        upload_to="jobs/contracts/",
        blank=True,
    )

    administration_note = models.TextField(
        blank=True,
    )

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_employment_contracts",
    )

    validated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    worker_acceptance_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    worker_accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    worker_acceptance_note = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contrat de travail"
        verbose_name_plural = "Contrats de travail"
        permissions = [
            (
                "review_employmentcontract",
                "Examiner un contrat de travail",
            ),
            (
                "validate_employmentcontract",
                "Valider un contrat de travail",
            ),
            (
                "accept_employmentcontract",
                "Enregistrer l'acceptation du travailleur",
            ),
        ]

    def __str__(self):
        return self.contract_number


class EmploymentContractAnnex(models.Model):

    STATUS_CHOICES = [
        ("SOUMISE", "Soumise"),
        ("VALIDEE", "Validée"),
        ("REFUSEE", "Refusée"),
    ]

    contract = models.ForeignKey(
        EmploymentContract,
        on_delete=models.CASCADE,
        related_name="annexes",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    document = models.FileField(
        upload_to="jobs/contracts/annexes/",
    )

    is_required = models.BooleanField(
        default=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="SOUMISE",
    )

    administration_note = models.TextField(
        blank=True,
    )

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_employment_contract_annexes",
    )

    validated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Annexe du contrat"
        verbose_name_plural = "Annexes des contrats"
        permissions = [
            (
                "review_employmentcontractannex",
                "Examiner une annexe de contrat",
            ),
            (
                "validate_employmentcontractannex",
                "Valider une annexe de contrat",
            ),
        ]

    def __str__(self):
        return f"{self.contract.contract_number} - {self.title}"
