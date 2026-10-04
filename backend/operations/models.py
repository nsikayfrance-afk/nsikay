from django.db import models



class DepositRequest(models.Model):

    STATUS = [

        ("pending","En attente"),

        ("validated","Validé"),

        ("completed","Terminé"),

        ("rejected","Refusé"),

    ]


    user = models.ForeignKey(

        "core.Profile",

        on_delete=models.CASCADE

    )


    partner = models.ForeignKey(

        "partner_finance.PartnerWallet",

        on_delete=models.PROTECT

    )


    amount = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )


    currency = models.ForeignKey(

        "finance.Currency",

        on_delete=models.PROTECT

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




class WithdrawalRequest(models.Model):


    STATUS = [

        ("pending","En attente"),

        ("approved","Approuvé"),

        ("completed","Terminé"),

        ("rejected","Refusé"),

    ]



    user = models.ForeignKey(

        "core.Profile",

        on_delete=models.CASCADE

    )


    partner = models.ForeignKey(

        "partner_finance.PartnerWallet",

        on_delete=models.PROTECT

    )


    amount = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )


    currency = models.ForeignKey(

        "finance.Currency",

        on_delete=models.PROTECT

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



class OperationApproval(models.Model):


    operation_type = models.CharField(

        max_length=50

    )


    operation_id = models.IntegerField()


    approved_by = models.CharField(

        max_length=100

    )


    decision = models.CharField(

        max_length=30

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )

