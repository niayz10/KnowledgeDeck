
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from auth_.views import User

urlpatterns = [
    path('login', obtain_jwt_token),
    path('register',  User.as_view({'post': 'create'})),
    path('profile', User.as_view({'get': 'get_information_about_yourself'})),
    path('list_of_users', User.as_view({'get': 'list_of_users'})),
]
