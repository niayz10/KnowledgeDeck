from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
from auth_.base_models import DeckMixin, CardMixin


class DeckTemplate(DeckMixin):
    pass

class CardTemplate(CardMixin):
    deck_template = models.ForeignKey(DeckTemplate, on_delete=models.CASCADE, related_name="deck_card_templates")
