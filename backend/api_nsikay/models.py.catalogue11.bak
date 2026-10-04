from api_nsikay.tv.models import TVChannel
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User



class UserRole(models.Model):


    ROLE_CHOICES = (

        ("CLIENT","Client"),

        ("AGENT","Agent NSIKAY"),

        ("BANK","Banque"),

        ("ADMIN","Administrateur"),

    )


    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE,

        related_name="nsikay_role"

    )


    role = models.CharField(

        max_length=20,

        choices=ROLE_CHOICES,

        default="CLIENT"

    )


    active = models.BooleanField(

        default=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class SecurityProfile(models.Model):


    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE,

        related_name="security_profile"

    )


    two_factor_enabled = models.BooleanField(

        default=False

    )


    last_login_ip = models.GenericIPAddressField(

        null=True,

        blank=True

    )


    failed_attempts = models.IntegerField(

        default=0

    )


    locked = models.BooleanField(

        default=False

    )


    updated_at = models.DateTimeField(

        auto_now=True

    )

from django.db import models
from django.contrib.auth.models import User



class CreatorProfile(models.Model):

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE,

        related_name="creator_profile"

    )

    verified = models.BooleanField(

        default=False

    )

    followers = models.IntegerField(

        default=0

    )

    earnings = models.DecimalField(

        max_digits=20,

        decimal_places=2,

        default=0

    )



class SocialPost(models.Model):

    author = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="posts"

    )

    content = models.TextField()

    image = models.URLField(

        blank=True

    )

    likes = models.IntegerField(

        default=0

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )



class SocialComment(models.Model):

    post = models.ForeignKey(

        SocialPost,

        on_delete=models.CASCADE,

        related_name="comments"

    )

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    message = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True

    )



class NsikayEvent(models.Model):

    organizer = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    title = models.CharField(

        max_length=255

    )

    description = models.TextField()

    date = models.DateTimeField()

    location = models.CharField(

        max_length=255

    )



class EventParticipant(models.Model):

    event = models.ForeignKey(

        NsikayEvent,

        on_delete=models.CASCADE

    )

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )



class AdvertisingCampaign(models.Model):

    owner = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    title = models.CharField(

        max_length=255

    )

    budget = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )

    active = models.BooleanField(

        default=True

    )

    views = models.IntegerField(

        default=0

    )



class AdvertisementPlacement(models.Model):

    campaign = models.ForeignKey(

        AdvertisingCampaign,

        on_delete=models.CASCADE,

        related_name="placements"

    )

    position = models.CharField(

        max_length=100

    )




    name = models.CharField(

        max_length=255

    )

    stream_url = models.URLField()

    active = models.BooleanField(

        default=True

    )



class TVContent(models.Model):

    channel = models.ForeignKey(

        TVChannel,

        on_delete=models.CASCADE

    )

    title = models.CharField(

        max_length=255

    )

    video_url = models.URLField()



class VirtualGift(models.Model):

    name = models.CharField(

        max_length=255

    )

    value = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )

    currency = models.CharField(

        max_length=10,

        default="USD"

    )



class GiftTransaction(models.Model):

    sender = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="sent_gifts"

    )

    receiver = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="received_gifts"

    )

    gift = models.ForeignKey(

        VirtualGift,

        on_delete=models.CASCADE

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )



class CreatorSubscription(models.Model):

    creator = models.ForeignKey(

        CreatorProfile,

        on_delete=models.CASCADE

    )

    subscriber = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    monthly_price = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )

    active = models.BooleanField(

        default=True

    )

from django.db import models
from django.contrib.auth.models import User



class ContentRecommendation(models.Model):


    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="recommendations"

    )


    content_type = models.CharField(

        max_length=100

    )


    content_id = models.IntegerField()


    score = models.DecimalField(

        max_digits=5,

        decimal_places=2,

        default=0

    )


    generated_at = models.DateTimeField(

        auto_now_add=True

    )



class ModerationRecord(models.Model):


    STATUS = (

        ("SAFE","Validé"),

        ("REVIEW","Contrôle"),

        ("BLOCKED","Bloqué"),

    )


    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )


    content_type = models.CharField(

        max_length=100

    )


    content_id = models.IntegerField()


    score_risk = models.IntegerField(

        default=0

    )


    status = models.CharField(

        max_length=20,

        choices=STATUS,

        default="SAFE"

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class ContentAnalytics(models.Model):


    content_type = models.CharField(

        max_length=100

    )


    content_id = models.IntegerField()


    views = models.IntegerField(

        default=0

    )


    likes = models.IntegerField(

        default=0

    )


    shares = models.IntegerField(

        default=0

    )


    revenue = models.DecimalField(

        max_digits=20,

        decimal_places=2,

        default=0

    )


    updated_at = models.DateTimeField(

        auto_now=True

    )



class AdCampaignCenter(models.Model):


    owner = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )


    title = models.CharField(

        max_length=255

    )


    target_country = models.CharField(

        max_length=100

    )


    target_category = models.CharField(

        max_length=100

    )


    budget = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )


    impressions = models.IntegerField(

        default=0

    )


    clicks = models.IntegerField(

        default=0

    )


    active = models.BooleanField(

        default=True

    )



class PagePromotionSlot(models.Model):


    PAGE_TYPES = (

        ("HOME","Accueil"),

        ("PROFILE","Profil"),

        ("TV","TV"),

        ("EVENT","Événement"),

        ("WENZE","WENZE"),

    )


    page_type = models.CharField(

        max_length=50,

        choices=PAGE_TYPES

    )


    campaign = models.ForeignKey(

        AdCampaignCenter,

        on_delete=models.CASCADE

    )


    active = models.BooleanField(

        default=True

    )



class EventPromotion(models.Model):


    event_id = models.IntegerField()


    campaign = models.ForeignKey(

        AdCampaignCenter,

        on_delete=models.CASCADE

    )


    start_date = models.DateTimeField()


    end_date = models.DateTimeField()



class AdminAnalytics(models.Model):


    metric = models.CharField(

        max_length=255

    )


    value = models.DecimalField(

        max_digits=20,

        decimal_places=2

    )


    category = models.CharField(

        max_length=100

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )

from django.db import models
from django.contrib.auth.models import User



class CountryConfiguration(models.Model):


    name = models.CharField(

        max_length=100

    )


    code = models.CharField(

        max_length=10,

        unique=True

    )


    currency = models.CharField(

        max_length=10

    )


    active = models.BooleanField(

        default=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class UserNotification(models.Model):


    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="notifications"

    )


    title = models.CharField(

        max_length=255

    )


    message = models.TextField()


    read = models.BooleanField(

        default=False

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class InternalMessage(models.Model):


    sender = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="sent_messages"

    )


    receiver = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="received_messages"

    )


    content = models.TextField()


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class CloudFile(models.Model):


    owner = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )


    file_name = models.CharField(

        max_length=255

    )


    file_url = models.URLField()


    file_type = models.CharField(

        max_length=100

    )


    size = models.BigIntegerField(

        default=0

    )


    private = models.BooleanField(

        default=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )



class APIGatewayLog(models.Model):


    endpoint = models.CharField(

        max_length=255

    )


    method = models.CharField(

        max_length=20

    )


    user = models.ForeignKey(

        User,

        null=True,

        blank=True,

        on_delete=models.SET_NULL

    )


    response_code = models.IntegerField()


    created_at = models.DateTimeField(

        auto_now_add=True

    )






