from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class DeckTemplate(models.Model):
    title = models.CharField(_('title'), max_length=30, blank=True)


class CardTemplate(models.Model):
    title = models.CharField(_('title'), max_length=30, blank=True)
    deck_template = models.ForeignKey(DeckTemplate, on_delete=models.CASCADE, related_name="deck_card_templates")
