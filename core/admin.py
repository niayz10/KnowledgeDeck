from django.contrib import admin

# Register your models here.
from core.models import CardTemplate, DeckTemplate

admin.site.register(CardTemplate)
admin.site.register(DeckTemplate)
