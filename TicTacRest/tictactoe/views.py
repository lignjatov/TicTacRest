from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from tictactoe.serializers import UserSerializer, GameSerializer
from django.contrib.auth.models import User
from tictactoe.models import TicTacToeGame
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    
class GameCreate(generics.CreateAPIView):
    queryset = TicTacToeGame
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]   
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class GamesList(generics.ListAPIView):
    queryset = TicTacToeGame.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class JoinGame(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def patch(self, request, game_id, format=None):
        joiningGame = get_object_or_404(TicTacToeGame, id=game_id)
        
        if joiningGame.opponent is not None:
            return Response({'error': 'Opponent has already entered'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = GameSerializer(instance=joiningGame, 
                                    partial=True, 
                                    data={'opponent': request.user.id, 'game_state': TicTacToeGame.GameState.IN_PROGRESS})
        if serializer.is_valid():
            serializer.save()
            return Response({'Success:': 'Game joined'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        