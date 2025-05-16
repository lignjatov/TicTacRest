from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from tictactoe.filters import GameFilter
from tictactoe.serializers import MoveSerializer, UserSerializer, GameSerializer
from tictactoe.models import TicTacToeGame
from tictactoe.utils import tictactoe
from drf_spectacular.utils import extend_schema

# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

class UserProfile(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'
    
class GameCreate(generics.CreateAPIView):
    queryset = TicTacToeGame
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated] 
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class GamesList(generics.ListAPIView):
    queryset = TicTacToeGame.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GameFilter
    ordering_fields = ['creation_time']
    ordering = ['-creation_time']


@extend_schema(request=None,
        responses={200: GameSerializer, 400: None, 403: None},  
        description="Join an available Tic Tac Toe game as the opponent.")
class JoinGame(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, game_id, format=None):
        joining_game = get_object_or_404(TicTacToeGame, id=game_id)
        
        if joining_game.opponent is not None:
            return Response({'error': 'Opponent has already entered'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = GameSerializer(instance=joining_game, 
                                    partial=True, 
                                    data={'opponent': request.user.id, 'game_state': TicTacToeGame.GameState.IN_PROGRESS})
        if serializer.is_valid():
            serializer.save()
            return Response({'Success:': 'Game joined'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_board_state(request, game_id):
    checking_game = get_object_or_404(TicTacToeGame, id=game_id)
    return Response({'game_board': checking_game.game_board})


@extend_schema(request=MoveSerializer)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def make_move(request, game_id):
    checking_game = get_object_or_404(TicTacToeGame, id=game_id)
    #Initial checks
    if checking_game.game_state != TicTacToeGame.GameState.IN_PROGRESS:
        return Response({'error': 'Game is not available.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.user.username != checking_game.creator.username and request.user.id != checking_game.opponent.id:
        return Response({'error': 'User is not participant in match.'}, status=status.HTTP_403_FORBIDDEN)
    
    #return Response(request.data)

    row = request.data.get('row')
    col = request.data.get('col')

    if row is None or col is None:
        return Response({'error': 'row and col must be defined!'}, status=status.HTTP_400_BAD_REQUEST)
    
    #Check turn
    sign = ''
    if not checking_game.player_turn and request.user.id == checking_game.creator.id:
        sign = 'x'
        turn_change_to = True
    elif checking_game.player_turn and request.user.id == checking_game.opponent.id:
        sign = 'o'
        turn_change_to = False
    else:
        return Response({'error': 'Not your turn'}, status=status.HTTP_403_FORBIDDEN)
    
    game = tictactoe(checking_game.game_board)
    
    move_valid = game.make_move(sign, int(request.data['row']), int(request.data['col']))
    if move_valid != None:
        return Response({'error:': move_valid}, status=status.HTTP_400_BAD_REQUEST)
        
    updated_data={'game_board': game.transform_board_to_line(), 'player_turn': turn_change_to, 'game_board': game.transform_board_to_line()}
    if game.is_finished() != False:
        updated_data.update({
            'game_state': TicTacToeGame.GameState.FINISHED,
            'winner': request.user.id
        })
      
        
    serializer = GameSerializer(instance=checking_game, 
                                    partial=True, 
                                    data=updated_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)