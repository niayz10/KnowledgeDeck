from rest_framework import serializers


class DeckMixinSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CardMixinSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
