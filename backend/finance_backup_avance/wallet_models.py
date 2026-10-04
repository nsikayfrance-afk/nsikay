from django.db import models



class Wallet(models.Model):

    owner = models.ForeignKey(

        "core.Profile",

        on_delete=models.CASCADE

    )


    currency = models.ForeignKey(

        "finance.Currency",

        on_delete=models.PROTECT

    )


    balance = models.DecimalField(

        max_digits=20,

        decimal_places=2,

        default=0

    )


    active = models.BooleanField(

        default=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    def __str__(self):

        return (

            str(self.owner)

            +

            " - "

            +

            self.currency.code

        )




class WalletOperation(models.Model):


    TYPES = [

        ("credit","Crédit"),

        ("debit","Débit"),

    ]


    wallet = models.ForeignKey(

        Wallet,

        on_delete=models.CASCADE

    )


    amount = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )


    operation_type = models.CharField(

        max_length=20,

        choices=TYPES

    )


    reference = models.CharField(

        max_length=100,

        unique=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )

