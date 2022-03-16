from auth_ import serializers
from core.models import DeckTemplate


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckTemplate
        fields = ('title')
