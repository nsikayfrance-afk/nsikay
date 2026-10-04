
from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()


class AdminActionLog(models.Model):

    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action=models.CharField(
        max_length=255
    )

    created=models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.action


class SecurityAlert(models.Model):

    message=models.CharField(
        max_length=255
    )

    active=models.BooleanField(
        default=True
    )

    created=models.DateTimeField(
        auto_now_add=True
    )
