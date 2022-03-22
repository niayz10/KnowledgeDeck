from abc import ABC

from rest_framework import serializers

from auth_.base_abstract_serializers import DeckMixinSerializer, CardMixinSerializer
from auth_.models import CustomUser, Deck, Card, ContentFragment, ContentFragmentForCard
from core.serializers import DeckTemplateSerializer, CardTemplateSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

    def validate_email(self, email):
        if '/^[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}$/i' in email:
            raise serializers.ValidationError("The email is not entered correctly")
        return email

    def validate_password(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError('Passwords must match')
        return value


class CustomUserSerializerAll(CustomUserSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserSerializerForComment(CustomUserSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name')


class ProfileSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=30)
    location = serializers.CharField(max_length=30)
    user = CustomUserSerializer(read_only=True)

    def create(self, validated_data):
        validated_data.setdefault('user', self.context.get('user'))
        return Deck.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance


class DeckSerializer(DeckMixinSerializer):
    id = serializers.IntegerField(read_only=True)
    progress = serializers.IntegerField(read_only=True)
    template = DeckTemplateSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)

    def create(self, validated_data):
        validated_data.setdefault('template', self.context.get('template'))
        validated_data.setdefault('profile', self.context.get('profile'))
        return Deck.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class CardSerializer(CardMixinSerializer):
    status = serializers.IntegerField(required=False)
    template = CardTemplateSerializer(read_only=True)
    deck = DeckSerializer(read_only=True)

    def validate_status(self, value):
        if 0 <= value <= 2:
            return value
        else:
            raise serializers.ValidationError("Invalid status")

    def create(self, validated_data):
        validated_data.setdefault('template', self.context.get('template'))
        validated_data.setdefault('deck', self.context.get('deck'))
        return Card.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.failed = validated_data.get('status', instance.status)
        instance.save()
        return instance


class ContentFragmentSerializer(serializers.Serializer):
    type = serializers.IntegerField()
    file = serializers.FileField()

    def create(self, validated_data):
        validated_data.setdefault('upload', self.context.get('card_template'))
        return ContentFragment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance


class ContentFragmentForCardSerializer(serializers.Serializer):
    type = serializers.IntegerField()
    file = serializers.FileField()

    def create(self, validated_data):
        validated_data.setdefault('upload', self.context.get('card'))
        return ContentFragmentForCard.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance
