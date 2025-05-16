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
@extend_schema(description="Listing for all users, only accessible by the admin.")
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

@extend_schema(description="User creation. It doesn't immediately authenticate the user as the application is using JWTAuthentication. Look at user/login and user/refresh for getting your tokens")
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

@extend_schema(description="Profile checking. Returns win rate, amount of games played and the username.")
class UserProfile(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'
  
@extend_schema(description="Game creation. No parameteres are needed. The authenticated user is set as the creator of the game and it sets itself into the Awaiting state",
               request=None)
class GameCreate(generics.CreateAPIView):
    queryset = TicTacToeGame
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated] 
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

@extend_schema(description="Retrieving all the data regarding games. It has options for filtering and ordering.")
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
        description="Join a Tic Tac Toe game as the opponent. Games are accessed through their ID. For starting a game, use the /game/open/ endpoint.")
class JoinGame(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, game_id, format=None):
        #first we need to find the game 
        joining_game = get_object_or_404(TicTacToeGame, id=game_id)
        
        #if the opponent spot was already taken, returns an error
        if joining_game.opponent is not None:
            return Response({'error': 'Opponent has already entered'}, status=status.HTTP_403_FORBIDDEN)
        
        #sets the opponent to the authenticated user and puts the game in progress
        serializer = GameSerializer(instance=joining_game, 
                                    partial=True, 
                                    data={'opponent': request.user.id, 'game_state': TicTacToeGame.GameState.IN_PROGRESS})
        if serializer.is_valid():
            serializer.save()
            return Response({'Success:': 'Game joined'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema(description="Returns the board state of a particular game.")
@api_view(['GET'])
def get_board_state(request, game_id):
    checking_game = get_object_or_404(TicTacToeGame, id=game_id)
    return Response({'game_board': checking_game.game_board})


@extend_schema(request=MoveSerializer,
               description="Endpoint for making a move. Expect row and col to be between and including 0 and 2",
               )
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def make_move(request, game_id):
    checking_game = get_object_or_404(TicTacToeGame, id=game_id)
    #Initial checks
    if checking_game.game_state != TicTacToeGame.GameState.IN_PROGRESS:
        return Response({'error': 'Game is not available.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.user.username != checking_game.creator.username and request.user.id != checking_game.opponent.id:
        return Response({'error': 'User is not participant in match.'}, status=status.HTTP_403_FORBIDDEN)

    #row and column played
    row = request.data.get('row')
    col = request.data.get('col')

    if row is None or col is None:
        return Response({'error': 'row and col must be defined!'}, status=status.HTTP_400_BAD_REQUEST)
    
    #Check whose turn it is. The creator is ALWAYS 'x' while the opponent is always 'o'.
    #Upon playing their turn, the variable turn_change_to changes to pass the turn in order to avoid multiple turns by the same user
    #Turn tracking is done through the player_turn attribute in the model.
    sign = ''
    if not checking_game.player_turn and request.user.id == checking_game.creator.id:
        sign = 'x'
        turn_change_to = True
    elif checking_game.player_turn and request.user.id == checking_game.opponent.id:
        sign = 'o'
        turn_change_to = False
    else:
        return Response({'error': 'Not your turn'}, status=status.HTTP_403_FORBIDDEN)
    
    #utils.tictactoe is called upon to run the game
    game = tictactoe(checking_game.game_board)
    
    #Players make their turn. If any error appears, it is reported back and the move is not saved
    move_valid = game.make_move(sign, int(row), int(col))
    if move_valid != None:
        return Response({'error:': move_valid}, status=status.HTTP_400_BAD_REQUEST)
        
    #In case the game is finished, additional data is added to saved object. The winner gets set and state is set to finished
    updated_data={'game_board': game.transform_board_to_line(), 'player_turn': turn_change_to, 'game_board': game.transform_board_to_line()}
    if game.is_finished() != False:
        updated_data.update({
            'game_state': TicTacToeGame.GameState.FINISHED,
            'winner': request.user.id
        })
      
    #Move saving
    serializer = GameSerializer(instance=checking_game, 
                                    partial=True, 
                                    data=updated_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)