from django.db import models
from django.contrib.auth.models import User


class MembershipType(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    contribution_required = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )


    def __str__(self):
        return self.name



class Member(models.Model):

    STATUS = (
        ("pending", "En attente"),
        ("active", "Actif"),
        ("suspended", "Suspendu"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    membership_type = models.ForeignKey(
        MembershipType,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS,
        default="pending"
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )



class Subscription(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="USD"
    )

    payment_status = models.CharField(
        max_length=50,
        default="pending"
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )



class Donation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="USD"
    )

    message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

