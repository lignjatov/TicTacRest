from django.urls import path
from tictactoe.serializers import UserSerializer
from tictactoe import views

urlpatterns = [
    path("user/", views.UserList.as_view()),
    path("user/register/", views.UserCreate.as_view()),
    #path("user/login/"),
    path("game/open", views.GameCreate.as_view()),
]
