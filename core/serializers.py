from auth_ import serializers
from core.models import DeckTemplate, CardTemplate
from rest_framework import serializers


class DeckTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckTemplate
        fields = ('title',)


class CardTemplateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    deck_template = DeckTemplateSerializer(read_only=True)

    def create(self, validated_data):
        validated_data.setdefault('deck_template', self.context.get('deck_template'))
        return CardTemplate.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
