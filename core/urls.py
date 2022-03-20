
from django.urls import path

from core.views import DeckTemplateViewSet, CardTemplateViewSet

urlpatterns = [
    path('deck_template', DeckTemplateViewSet.as_view({'get': 'list_of_all_deck_templates',
                                                       'post': 'create_deck_template'})),
    path('deck_template/<int:id>', DeckTemplateViewSet.as_view({'put': 'update_deck_template',
                                                                'delete': 'destroy_deck_template'})),
    path('card_template', CardTemplateViewSet.as_view({'get': 'list_of_all_card_templates',
                                                        'post': 'create_card_template'})),
    path('card_template/<int:id>', CardTemplateViewSet.as_view({'put': 'update_card_template',
                                                                'delete': 'destroy_card_template'})),
]
