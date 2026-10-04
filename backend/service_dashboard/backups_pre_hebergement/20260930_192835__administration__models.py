from django.db import models



class BankCertification(models.Model):

    STATUS = [

        ("pending","En attente"),

        ("approved","Approuvée"),

        ("rejected","Refusée"),

    ]


    bank = models.ForeignKey(

        "banking.Bank",

        on_delete=models.CASCADE,
        related_name="bank_certification_relation"
    )


    documents = models.TextField()


    status = models.CharField(

        max_length=30,

        choices=STATUS,

        default="pending"

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )




class CurrencyApproval(models.Model):


    currency = models.ForeignKey(

        "finance.Currency",

        on_delete=models.CASCADE,
        related_name="currency_approval_relation"
    )


    bank = models.ForeignKey(

        "banking.Bank",

        on_delete=models.CASCADE,
        related_name="currency_approval_relation"
    )


    status = models.CharField(

        max_length=30,

        default="pending"

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )




class PartnerCertification(models.Model):


    partner = models.ForeignKey(

        "partner_finance.PartnerApplication",

        on_delete=models.CASCADE,
        related_name="currency_approval_relation"
    )


    status = models.CharField(

        max_length=30,

        default="pending"

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )




class CountrySupervision(models.Model):


    country_name = models.CharField(

        max_length=100

    )


    code = models.CharField(

        max_length=10

    )


    active = models.BooleanField(

        default=True

    )


    banks_count = models.IntegerField(

        default=0

    )


    partners_count = models.IntegerField(

        default=0

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class ValidationRequest(models.Model):

    REQUEST_TYPES = (
        ("bank", "Certification Banque"),
        ("currency", "Validation Devise"),
        ("partner", "Validation Partenaire Financier"),
        ("country", "Supervision Pays"),
    )

    request_type = models.CharField(
        max_length=50,
        choices=REQUEST_TYPES
    )

    applicant = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.request_type









class BankCountryAccess(models.Model):

    bank_name = models.CharField(
        max_length=255
    )

    country_name = models.CharField(
        max_length=255
    )

    access_level = models.CharField(
        max_length=100,
        default="STANDARD"
    )

    status = models.CharField(
        max_length=50,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.bank_name} - {self.country_name}"




class BankCurrencyAccess(models.Model):

    bank_name = models.CharField(
        max_length=255
    )

    currency = models.CharField(
        max_length=50
    )

    access_level = models.CharField(
        max_length=100,
        default="STANDARD"
    )

    status = models.CharField(
        max_length=50,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.bank_name} - {self.currency}"



class BankServiceAuthorization(models.Model):

    bank_name = models.CharField(
        max_length=255
    )

    service_name = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=50,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.bank_name} - {self.service_name}"



class CountryBankAuthorization(models.Model):

    country_name = models.CharField(
        max_length=255
    )

    bank_name = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=50,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.country_name} - {self.bank_name}"



# ================================
# BANQUES PARTENAIRES NSIKAY
# ================================

from django.db import models


class BankPartner(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True
    )

    country = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    certified = models.BooleanField(
        default=False
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.name



class BankPartnerCurrency(models.Model):

    bank = models.ForeignKey(
        BankPartner,
        on_delete=models.CASCADE
    )

    currency = models.CharField(
        max_length=10
    )

    active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.bank} - {self.currency}"



class BankPartnerService(models.Model):

    SERVICES = [
        ("deposit","Dépôt"),
        ("withdraw","Retrait"),
        ("transfer","Transfert"),
        ("exchange","Change"),
        ("wallet","Wallet"),
    ]


    bank = models.ForeignKey(
        BankPartner,
        on_delete=models.CASCADE
    )

    service = models.CharField(
        max_length=50,
        choices=SERVICES
    )

    active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.bank} - {self.service}"



# ===============================
# SUPERVISION PAYS NSIKAY
# ===============================


class CountryCurrencyAccess(models.Model):

    country = models.ForeignKey(
        CountrySupervision,
        on_delete=models.CASCADE
    )

    currency = models.CharField(
        max_length=10
    )

    active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.country} - {self.currency}"




class CountryRegulation(models.Model):

    country = models.OneToOneField(
        CountrySupervision,
        on_delete=models.CASCADE
    )

    authority = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    regulation_status = models.CharField(
        max_length=50,
        default="active"
    )


    def __str__(self):
        return str(self.country)



class CountryBankAccess(models.Model):

    country = models.ForeignKey(
        CountrySupervision,
        on_delete=models.CASCADE
    )

    bank = models.ForeignKey(
        "BankPartner",
        on_delete=models.CASCADE
    )

    authorized = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.country} - {self.bank}"



# =====================================================
# SUPERVISION PAYS NSIKAY
# =====================================================

class CountrySupervisionDetail(models.Model):

    pays = models.CharField(max_length=100)

    code_iso = models.CharField(
        max_length=10,
        unique=True
    )

    actif = models.BooleanField(
        default=True
    )

    banques_autorisees = models.ManyToManyField(
        "BankPartner",
        blank=True
    )

    devises_autorisees = models.JSONField(
        default=list
    )

    niveau_conformite = models.CharField(
        max_length=50,
        default="en_verification"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.pays




from django.conf import settings
from django.db import models


class NSIKAYAdminRole(models.Model):

    ROLE_CHOICES = [

        ("SUPER_ADMIN", "Super Administrateur NSIKAY"),

        ("BANK_ADMIN", "Administrateur Banque"),

        ("COUNTRY_ADMIN", "Administrateur Pays"),

        ("CERTIFICATION_ADMIN", "Administrateur Certification"),

        ("FINANCE_ADMIN", "Administrateur Finance"),

    ]


    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )


    active = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return f"{self.user} - {self.role}"



class NSIKAYPermission(models.Model):


    role = models.ForeignKey(
        NSIKAYAdminRole,
        on_delete=models.CASCADE
    )


    module = models.CharField(
        max_length=100
    )


    can_view = models.BooleanField(
        default=False
    )


    can_create = models.BooleanField(
        default=False
    )


    can_update = models.BooleanField(
        default=False
    )


    can_delete = models.BooleanField(
        default=False
    )


    def __str__(self):

        return self.module

class HealthInsurance(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("validated", "Validee"),
        ("expired", "Expiree"),
        ("rejected", "Refusee"),
    ]

    insured_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="health_insurances",
    )
    provider_name = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    validated_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["insured_user", "status"]),
            models.Index(fields=["country", "status"]),
            models.Index(fields=["policy_number"]),
        ]

    def __str__(self):
        return f"{self.provider_name} - {self.policy_number}"

    @property
    def is_valid(self):
        from django.utils import timezone

        today = timezone.localdate()

        return (
            self.status == "validated"
            and self.validated_by_admin
            and self.start_date <= today <= self.end_date
        )

