from django.contrib import admin

# Register your models here.
from auth_.models import CustomUser, Profile, Deck, Card, ContentFragment

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(ContentFragment)