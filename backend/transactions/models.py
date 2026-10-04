from django.db import models



class Transaction(models.Model):

    TYPES = [

        ("transfer","Transfert"),

        ("withdrawal","Retrait"),

        ("payment","Paiement"),

        ("deposit","Dépôt"),

    ]


    STATUS = [

        ("pending","En attente"),

        ("completed","Terminé"),

        ("cancelled","Annulé"),

    ]


    sender = models.ForeignKey(
        "core.Profile",
        on_delete=models.PROTECT,
        related_name="sent_transactions"
    )


    receiver = models.ForeignKey(
        "core.Profile",
        on_delete=models.PROTECT,
        related_name="received_transactions",
        null=True,
        blank=True
    )


    partner = models.ForeignKey(
        "partner_finance.PartnerWallet",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )


    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )


    currency = models.ForeignKey(
        "finance.Currency",
        on_delete=models.PROTECT
    )


    transaction_type = models.CharField(
        max_length=30,
        choices=TYPES
    )


    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="pending"
    )


    reference = models.CharField(
        max_length=100,
        unique=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

