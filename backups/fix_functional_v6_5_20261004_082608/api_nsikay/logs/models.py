from django.db import models
from django.conf import settings


class AdminSecurityLog(models.Model):


    ACTIONS = [

        ("LOGIN","LOGIN"),

        ("ACCESS","ACCESS"),

        ("CREATE","CREATE"),

        ("UPDATE","UPDATE"),

        ("DELETE","DELETE"),

    ]


    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        null=True,

        on_delete=models.SET_NULL

    )


    action = models.CharField(

        max_length=50,

        choices=ACTIONS

    )


    ip_address = models.GenericIPAddressField(

        null=True,

        blank=True

    )


    details = models.TextField(

        blank=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


