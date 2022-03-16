
import logging
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from auth_.models import CustomUser
from auth_.serializers import CustomUserSerializer, CustomUserSerializerAll
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

logger = logging.getLogger(__name__)


class User(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def list_of_users(self, request):
        logger.info('list of a users')
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
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
