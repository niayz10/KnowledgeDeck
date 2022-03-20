
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from auth_.views import User, DeckViewSet, CardViewSet

urlpatterns = [
    path('login', obtain_jwt_token),
    path('register',  User.as_view({'post': 'create_user'})),
    path('profile', User.as_view({'get': 'get_information_about_yourself'})),
    path('list_of_users', User.as_view({'get': 'list_of_users'})),
    path('deck', DeckViewSet.as_view({'get': 'list_of_all_decks', 'post': 'create_deck'})),
    path('deck/<int:id>', DeckViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('deck/cards_by_deck/<int:id>', DeckViewSet.as_view({'get': 'get_cards_by_deck'})),
    path('card', CardViewSet.as_view({'get': 'list_of_all_cards', 'post': 'create_card'})),
    path('card/<int:id>', CardViewSet.as_view({'put': 'update_card', 'delete': 'destroy_card'})),
]
