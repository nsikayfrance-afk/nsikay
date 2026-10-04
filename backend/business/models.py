from django.db import models
from django.contrib.auth.models import User


class Sector(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name



class Company(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True
    )

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    logo = models.URLField(
        blank=True
    )

    verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.name



class Employee(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    position = models.CharField(
        max_length=100
    )

    active = models.BooleanField(
        default=True
    )

