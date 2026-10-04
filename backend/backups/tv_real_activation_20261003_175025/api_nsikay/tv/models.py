from django.db import models


class TVChannel(models.Model):

    CATEGORIES = [
        ("economie","Économie"),
        ("sport","Sport & Loisirs"),
        ("culture","Culture & Arts"),
        ("technologie","Technologie & Innovation"),
        ("agriculture","Agriculture & Agronomie"),
        ("social","Social"),
        ("religion","Religion & Histoire"),
        ("adult","+18"),
    ]

    title = models.CharField(max_length=255)

    category = models.CharField(
        max_length=50,
        choices=CATEGORIES
    )

    description = models.TextField(
        blank=True
    )

    video_url = models.URLField()

    thumbnail = models.URLField(
        blank=True
    )

    is_live = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )


    created_at=models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.title

