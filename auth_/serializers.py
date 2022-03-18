from abc import ABC

from rest_framework import serializers
from auth_.models import CustomUser, Deck, Card
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


class DeckSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
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


class CardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    failed = serializers.BooleanField()
    template = CardTemplateSerializer(read_only=True)
    deck = DeckSerializer(read_only=True)

    def create(self, validated_data):
        validated_data.setdefault('template', self.context.get('template'))
        validated_data.setdefault('deck', self.context.get('deck'))
        return Card.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.failed = validated_data.get('failed', instance.failed)
        instance.save()
        return instance
