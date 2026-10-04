from django.db import models
from django.contrib.auth.models import User


class NsikayCountry(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ActivityDomain(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ActorProfile(models.Model):
    ACTOR_TYPES = [
        ('person', 'Personne'),
        ('company', 'Entreprise'),
        ('organization', 'Organisation'),
        ('bank', 'Banque'),
        ('agent', 'Agent'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    country = models.ForeignKey(
        NsikayCountry,
        on_delete=models.CASCADE
    )

    activity = models.ForeignKey(
        ActivityDomain,
        on_delete=models.CASCADE
    )

    actor_type = models.CharField(
        max_length=20,
        choices=ACTOR_TYPES
    )

    certified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ActorCertification(models.Model):
    STATUS = [
        ('pending', 'En attente'),
        ('approved', 'Validée'),
        ('rejected', 'Refusée'),
        ('expired', 'Expirée'),
    ]

    actor = models.ForeignKey(
        ActorProfile,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pending'
    )

    issued_date = models.DateField(
        auto_now_add=True
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    validator = models.CharField(
        max_length=150,
        blank=True
    )

    def __str__(self):
        return f'{self.actor} - {self.status}'


