from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Reseller(models.Model):
    """
    Statut officiel unique :
    Revendeur Cadeaux NSIKAY.
    """

    STATUS = (
        ("PENDING", "En attente"),
        ("ACTIVE", "Actif"),
        ("SUSPENDED", "Suspendu"),
        ("CLOSED", "Ferme"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="nsikay_gift_reseller",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="PENDING",
        db_index=True,
    )

    reseller_code = models.CharField(
        max_length=80,
        unique=True,
        db_index=True,
    )

    country_code = models.CharField(
        max_length=10,
        default="",
        blank=True,
    )

    notes = models.TextField(
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reseller_code} - {self.user}"

    class Meta:
        ordering = ["reseller_code"]


class ResellerNetwork(models.Model):
    """
    Réseau commercial créé par un revendeur.
    Les membres du réseau ne deviennent pas automatiquement revendeurs officiels.
    """

    principal_reseller = models.ForeignKey(
        Reseller,
        on_delete=models.PROTECT,
        related_name="networks",
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=80,
        unique=True,
        db_index=True,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NetworkMember(models.Model):
    """
    Membre commercial du réseau.
    Ce statut ne constitue pas un statut officiel de Revendeur NSIKAY.
    """

    network = models.ForeignKey(
        ResellerNetwork,
        on_delete=models.PROTECT,
        related_name="members",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="gift_network_memberships",
    )

    active = models.BooleanField(
        default=True,
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["network", "user"],
                name="uniq_gift_network_member",
            )
        ]

    def __str__(self):
        return f"{self.network.code} - {self.user}"


class GiftInventoryUnit(models.Model):
    """
    Unité individuelle d'un cadeau.

    La valeur officielle EUR est figée au moment de la création de l'unité.
    Le prix commercial peut évoluer indépendamment.
    """

    STATUS = (
        ("AVAILABLE", "Disponible"),
        ("DISTRIBUTED", "Distribue"),
        ("SOLD", "Vendu"),
        ("EXCHANGED", "Echange"),
        ("REDEEMED", "Utilise"),
        ("BLOCKED", "Bloque"),
    )

    SOURCE = (
        ("NSIKAY", "NSIKAY"),
        ("RESELLER", "Revendeur"),
        ("CREDIT", "Credit"),
        ("EXCHANGE", "Echange"),
    )

    unit_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    gift = models.ForeignKey(
        "api_nsikay.VirtualGift",
        on_delete=models.PROTECT,
        related_name="inventory_units",
    )

    official_value_eur = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    currency_reference = models.CharField(
        max_length=3,
        default="EUR",
    )

    current_reseller = models.ForeignKey(
        Reseller,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="gift_units",
    )

    current_member = models.ForeignKey(
        NetworkMember,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="gift_units",
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE,
        default="NSIKAY",
    )

    credit_only = models.BooleanField(
        default=False,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="AVAILABLE",
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.official_value_eur < Decimal("0.10"):
            raise ValidationError("La valeur officielle minimale est 0,10 EUR.")

        if self.official_value_eur > Decimal("100000.00"):
            raise ValidationError("La valeur officielle maximale est 100000 EUR.")

        if self.credit_only and self.source != "CREDIT":
            raise ValidationError(
                "Un cadeau credit_only doit provenir de la source CREDIT."
            )

    def __str__(self):
        return f"{self.unit_id} - {self.gift.name}"


class DistributionAgreement(models.Model):
    """
    Accord commercial défini avant la vente.
    Une fois LOCKED, les conditions historiques ne sont plus modifiables.
    """

    STATUS = (
        ("DRAFT", "Brouillon"),
        ("PENDING_ACCEPTANCE", "En attente d'acceptation"),
        ("ACCEPTED", "Accepte"),
        ("LOCKED", "Verrouille"),
        ("CANCELLED", "Annule"),
    )

    principal_reseller = models.ForeignKey(
        Reseller,
        on_delete=models.PROTECT,
        related_name="distribution_agreements",
    )

    network_member = models.ForeignKey(
        NetworkMember,
        on_delete=models.PROTECT,
        related_name="distribution_agreements",
    )

    gift = models.ForeignKey(
        "api_nsikay.VirtualGift",
        on_delete=models.PROTECT,
        related_name="distribution_agreements",
    )

    quantity = models.PositiveIntegerField()

    official_value_eur = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    member_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=3,
    )

    principal_reseller_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=3,
    )

    nsikay_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        default=Decimal("5.000"),
    )

    other_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        default=Decimal("0.000"),
    )

    effective_from = models.DateTimeField()
    effective_until = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=25,
        choices=STATUS,
        default="DRAFT",
        db_index=True,
    )

    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    locked_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    version = models.PositiveIntegerField(
        default=1,
    )

    previous_agreement = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="next_versions",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        percentages = (
            self.member_percentage
            + self.principal_reseller_percentage
            + self.other_percentage
        )

        if self.member_percentage < 0:
            raise ValidationError("Le pourcentage membre ne peut pas etre negatif.")

        if self.principal_reseller_percentage < 0:
            raise ValidationError(
                "Le pourcentage du revendeur principal ne peut pas etre negatif."
            )

        if self.nsikay_percentage != Decimal("5.000"):
            raise ValidationError(
                "La commission revendeur NSIKAY est fixee a 5 %."
            )

        if percentages > Decimal("100.000"):
            raise ValidationError(
                "La somme des pourcentages contractuels depasse 100 %."
            )

        if self.quantity <= 0:
            raise ValidationError("La quantite doit etre superieure a zero.")

        if self.status == "LOCKED" and not self.locked_at:
            raise ValidationError(
                "Un accord LOCKED doit posseder une date de verrouillage."
            )

    def __str__(self):
        return f"Accord {self.id} v{self.version} - {self.status}"


class ResellerSale(models.Model):
    """
    Vente d'un cadeau par le circuit revendeur.
    Le prix retail est distinct de la valeur officielle NSIKAY.
    """

    STATUS = (
        ("PENDING", "En attente"),
        ("PAID", "Payee"),
        ("SETTLED", "Reglee"),
        ("CANCELLED", "Annulee"),
        ("REFUNDED", "Remboursee"),
    )

    reference = models.CharField(
        max_length=120,
        unique=True,
        db_index=True,
    )

    gift_unit = models.ForeignKey(
        GiftInventoryUnit,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    agreement = models.ForeignKey(
        DistributionAgreement,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    network_member = models.ForeignKey(
        NetworkMember,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    principal_reseller = models.ForeignKey(
        Reseller,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="gift_purchases",
    )

    official_value_eur = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    retail_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    retail_currency = models.CharField(
        max_length=3,
        default="EUR",
    )

    nsikay_base_eur = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    nsikay_amount_eur = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    member_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
    )

    principal_reseller_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
    )

    other_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="PENDING",
        db_index=True,
    )

    payment_reference = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    settled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]


class SaleAllocation(models.Model):
    """
    Décomposition financière immuable d'une vente.
    """

    ALLOCATION_TYPES = (
        ("MEMBER", "Part membre"),
        ("PRINCIPAL_RESELLER", "Part revendeur principal"),
        ("NSIKAY", "Part NSIKAY"),
        ("OTHER", "Autre part"),
    )

    sale = models.ForeignKey(
        ResellerSale,
        on_delete=models.PROTECT,
        related_name="allocations",
    )

    allocation_type = models.CharField(
        max_length=30,
        choices=ALLOCATION_TYPES,
    )

    percentage = models.DecimalField(
        max_digits=8,
        decimal_places=3,
    )

    base_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=3,
        default="EUR",
    )

    reference = models.CharField(
        max_length=150,
        unique=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]


class GiftResellerAuditLog(models.Model):
    ACTIONS = (
        ("CREATED", "Cree"),
        ("DISTRIBUTED", "Distribue"),
        ("AGREEMENT_ACCEPTED", "Accord accepte"),
        ("AGREEMENT_LOCKED", "Accord verrouille"),
        ("SOLD", "Vendu"),
        ("ALLOCATED", "Repartition"),
        ("TRANSFERRED", "Transfere"),
        ("EXCHANGED", "Echange"),
        ("BLOCKED", "Bloque"),
    )

    action = models.CharField(
        max_length=30,
        choices=ACTIONS,
        db_index=True,
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="gift_reseller_audit_actions",
    )

    reference = models.CharField(
        max_length=150,
        db_index=True,
    )

    details = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]