
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from auth_.views import User, Deck

urlpatterns = [
    path('login', obtain_jwt_token),
    path('register',  User.as_view({'post': 'create_user'})),
    path('profile', User.as_view({'get': 'get_information_about_yourself'})),
    path('list_of_users', User.as_view({'get': 'list_of_users'})),
    path('deck', Deck.as_view({'get': 'list_of_decks', 'post': 'create_deck'})),
    path('deck/<int:id>', Deck.as_view({'put': 'update', 'delete': 'destroy'}))
]
