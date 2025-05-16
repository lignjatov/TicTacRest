from rest_framework import serializers
from tictactoe.models import TicTacToeGame
from django.contrib.auth.models import User
from django.db.models import Q


class GameSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    opponent_name = serializers.CharField(source='opponent.username', read_only=True)
    winner_name = serializers.CharField(source='winner.username', read_only=True)
    class Meta:
        model = TicTacToeGame
        fields = ['creation_time', 'game_state', 'creator', 'opponent', 'opponent_name','game_board', 'winner', 'winner_name', 'player_turn']  
    
class MoveSerializer(serializers.Serializer):
    row = serializers.IntegerField(min_value=0, max_value=2)
    col = serializers.IntegerField(min_value=0, max_value=2)
    
class UserSerializer(serializers.ModelSerializer):
    games = serializers.SerializerMethodField()
    won_games_percentage = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'games', 'won_games_percentage']
        
    def get_games(self, obj):
        games = TicTacToeGame.objects.filter(Q(creator=obj) | Q(opponent=obj)).count()
        #return GameSerializer(games, many=True).data
        return games
    
    def get_won_games_percentage(self, obj):
        won_games = TicTacToeGame.objects.filter(winner=obj).count()
        games = TicTacToeGame.objects.filter(Q(creator=obj) | Q(opponent=obj)).count()
        if games == 0:
            return 0.0
        
        won_games_percent = (won_games/games)*100
        return round(won_games_percent, 1)
        
    def create(self, validated_data):
        password = validated_data['password']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user