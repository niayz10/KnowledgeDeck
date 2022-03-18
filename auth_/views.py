import logging
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from auth_.models import CustomUser, Deck, Profile
from auth_.serializers import CustomUserSerializer, CustomUserSerializerAll, DeckSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from core.models import DeckTemplate

logger = logging.getLogger(__name__)


class User(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def list_of_users(self, request):
        logger.info('list of a users')
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def create_user(self, request):
        logger.info('Registration of a user')
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        user = CustomUser.objects.create_user(email, password, first_name=first_name, last_name=last_name)
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data)

    def get_information_about_yourself(self, request):
        logger.debug('Profile of the current user')
        print(request.user.is_anonymous)
        serializer = CustomUserSerializerAll(request.user, many=False)
        return Response(serializer.data)


class Deck(viewsets.ViewSet):

    def list_of_decks(self, request):
        logger.info('list of decks')
        decks = Deck.objects.all()
        serializer = DeckSerializer(decks, many=True)
        return Response(serializer.data)

    def create_deck(self, request):
        logger.info('Creation new deck')
        serializer = DeckSerializer(data=request.data, context={
            "template": DeckTemplate.objects.get(id=request.data.get('template_id')),
            'profile': request.user.profile
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, id):
        logger.info("Modifing deck")
        serializer = DeckSerializer(instance=Deck.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        logger.info('destroy a type')
        deck = Deck.objects.get(id=id)
        deck.delete()
        return Response('succes', status=status.HTTP_200_OK)
