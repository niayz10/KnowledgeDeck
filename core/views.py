from django.shortcuts import render

from rest_framework import viewsets, status

# Create your views here.
from rest_framework.response import Response

from auth_.serializers import ContentFragmentSerializer
from core.models import DeckTemplate, CardTemplate
from core.serializers import DeckTemplateSerializer, CardTemplateSerializer


class DeckTemplateViewSet(viewsets.ViewSet):

    def list_of_all_deck_templates(self, request):
        deck_templates = DeckTemplate.objects.all()
        serializer = DeckTemplateSerializer(deck_templates, many=True)
        return Response(serializer.data)

    def create_deck_template(self, request):
        serializer = DeckTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_deck_template(self, request, id):
        serializer = DeckTemplateSerializer(instance=DeckTemplate.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy_deck_template(self, request, id):
        deck_template = DeckTemplate.objects.get(id=id)
        deck_template.delete()
        return Response('success', status=status.HTTP_200_OK)


class CardTemplateViewSet(viewsets.ViewSet):

    def list_of_all_card_templates(self, request):
        card_templates = CardTemplate.objects.all()
        serializer = CardTemplateSerializer(card_templates, many=True)
        return Response(serializer.data)

    def create_card_template(self, request):
        serializer = CardTemplateSerializer(data=request.data, context={
            "deck_template": DeckTemplate.objects.get(id=request.data.get('deck_template_id'))
        })
        if serializer.is_valid():
            serializer.save()
            content_fragment = ContentFragmentSerializer(data=request.data, context={
                'card_template': CardTemplate.objects.get(id=serializer.data.get("id"))
            })
            if content_fragment.is_valid():
                content_fragment.save()
                return Response(content_fragment.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_card_template(self, request, id):
        serializer = CardTemplateSerializer(instance=CardTemplate.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy_card_template(self, request, id):
        card_tempalate = CardTemplate.objects.get(id=id)
        card_tempalate.delete()
        return Response('success', status=status.HTTP_200_OK)
