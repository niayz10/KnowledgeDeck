
from auth_.base_abstract_serializers import DeckMixinSerializer, CardMixinSerializer
from core.models import DeckTemplate, CardTemplate


class DeckTemplateSerializer(DeckMixinSerializer):
    class Meta:
        model = DeckTemplate
        fields = ('title',)

    def create(self, validated_data):
        return DeckTemplate.objects.create(**validated_data)


class CardTemplateSerializer(CardMixinSerializer):
    deck_template = DeckTemplateSerializer(read_only=True)

    def create(self, validated_data):
        validated_data.setdefault('deck_template', self.context.get('deck_template'))
        return CardTemplate.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
