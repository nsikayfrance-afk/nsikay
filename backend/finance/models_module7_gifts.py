from django.db import models


class VirtualGift(models.Model):

    VALUES = (
        ("0.50","0.50"),
        ("1","1"),
        ("5","5"),
        ("10","10"),
        ("50","50"),
        ("100","100"),
        ("500","500"),
        ("1000","1000"),
        ("2500","2500"),
        ("5000","5000"),
    )

    name = models.CharField(
        max_length=100
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.name



class GiftTransaction(models.Model):

    sender_wallet = models.IntegerField()

    receiver_wallet = models.IntegerField()

    gift = models.ForeignKey(
        VirtualGift,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    status = models.CharField(
        max_length=50,
        default="completed"
    )

    reference = models.CharField(
        max_length=255,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.reference



class GiftAuditLog(models.Model):

    action = models.CharField(
        max_length=255
    )

    details = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.action
