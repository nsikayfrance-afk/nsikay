from django.db import models
from django.contrib.auth.models import User


class MediaContent(models.Model):
    TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('tv', 'TV'),
        ('interview', 'Interview'),
        ('reportage', 'Reportage'),
        ('communique', 'Communique'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='media/content/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='media/thumbnails/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=30, default='draft')
    published_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class TVChannel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='media/tv/', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TVProgram(models.Model):
    channel = models.ForeignKey(TVChannel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    schedule = models.DateTimeField()

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=30, default='pending')

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

