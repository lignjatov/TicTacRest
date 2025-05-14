from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from tictactoe.serializers import UserSerializer, GameSerializer
from django.contrib.auth.models import User
from tictactoe.models import TicTacToeGame


# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    
class GameCreate(generics.CreateAPIView):
    queryset = TicTacToeGame
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        