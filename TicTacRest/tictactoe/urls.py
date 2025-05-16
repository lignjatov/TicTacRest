from django.urls import path
from tictactoe.serializers import UserSerializer
from tictactoe import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    #authentication operation
    path("user/", views.UserList.as_view()),
    path("user/<str:username>/profile/", views.UserProfile.as_view()),
    path("user/register/", views.UserCreate.as_view(), name="user-registration"),
    path("user/login/", TokenObtainPairView.as_view(), name="user-login"),
    path("user/refresh/", TokenRefreshView.as_view(), name="user-refresh"),
    #game operations
    path("game/",views.GamesList.as_view(), name="game-all"),
    path("game/open/", views.GameCreate.as_view(), name="game-open"),
    path("game/<int:game_id>/join/", views.JoinGame.as_view(), name="game-join"),
    path("game/<int:game_id>/board/", views.get_board_state, name="game-board"),
    path("game/<int:game_id>/move/", views.make_move, name="game-move"),
    #drf-spectacular urls:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]
