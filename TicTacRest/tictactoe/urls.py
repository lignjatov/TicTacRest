from django.urls import path
from tictactoe.serializers import UserSerializer
from tictactoe import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    #authentication operation
    path("user/", views.UserList.as_view()),
    path("user/<str:username>/profile", views.UserProfile.as_view()),
    path("user/register/", views.UserCreate.as_view()),
    path("user/login/", TokenObtainPairView.as_view()),
    path("user/refresh/", TokenRefreshView.as_view()),
    #Game operations
    path("game/",views.GamesList.as_view()),
    path("game/open/", views.GameCreate.as_view()),
    path("game/<int:game_id>/join/", views.JoinGame.as_view()),
    path("game/<int:game_id>/board/", views.get_board_state),
    path("game/<int:game_id>/move/", views.make_move),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]
