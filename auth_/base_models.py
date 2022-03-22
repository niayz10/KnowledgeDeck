from django.contrib.postgres.fields import ArrayField
from django.db import models

from utils.constants import CONTENT_TYPES


class DeckMixin(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True


class CardMixin(models.Model):
    title = models.CharField(max_length=255)
    front = models.TextField()
    back = models.TextField()

    class Meta:
        abstract = True


class ContentMixin(models.Model):
    type = models.SmallIntegerField(choices=CONTENT_TYPES)
    file = models.FileField(upload_to="contents")
    upload = models.ForeignKey(CardMixin, related_name="contents", on_delete=models.CASCADE)

    class Meta:
        abstract = True
