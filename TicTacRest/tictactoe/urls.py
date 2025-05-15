from django.urls import path
from tictactoe.serializers import UserSerializer
from tictactoe import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #authentication operation
    path("user/", views.UserList.as_view()),
    path("user/register/", views.UserCreate.as_view()),
    path("user/login/", TokenObtainPairView.as_view()),
    path("user/refresh/", TokenRefreshView.as_view()),
    #Game operations
    path("game/",views.GamesList.as_view()),
    path("game/open", views.GameCreate.as_view()),
    path("game/<int:game_id>/join/", views.JoinGame.as_view()),
]
