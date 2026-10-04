from django.db import models
from django.conf import settings


class KYCProfile(models.Model):

    STATUS = [

        ("PENDING","PENDING"),
        ("VERIFIED","VERIFIED"),
        ("REJECTED","REJECTED"),

    ]


    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE

    )


    status = models.CharField(

        max_length=20,

        choices=STATUS,

        default="PENDING"

    )


    document_type = models.CharField(

        max_length=50,

        blank=True

    )


    document_number = models.CharField(

        max_length=100,

        blank=True

    )


    verified_at = models.DateTimeField(

        null=True,

        blank=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    def is_verified(self):

        return self.status == "VERIFIED"


