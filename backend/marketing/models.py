from django.db import models
from django.contrib.auth.models import User


class Advertiser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    company_name = models.CharField(max_length=255)
    certification_status = models.CharField(max_length=50, default='pending')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class AdvertisingCampaign(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return self.title


class AdvertisementPlacement(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    campaign = models.ForeignKey(AdvertisingCampaign, on_delete=models.CASCADE)
    placement = models.ForeignKey(AdvertisementPlacement, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='marketing/images/', blank=True, null=True)
    video = models.FileField(upload_to='marketing/videos/', blank=True, null=True)
    link = models.URLField(blank=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return self.title


class AdvertisementStatistic(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

