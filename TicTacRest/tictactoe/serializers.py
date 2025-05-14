from rest_framework import serializers
from tictactoe.models import TicTacToeGame
from django.contrib.auth.models import User


class GameSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = TicTacToeGame
        fields = ['game_state', 'creator', 'opponent', 'game_board', 'winner', 'player_turn']  
    
    
class UserSerializer(serializers.ModelSerializer):
    games = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'games']
    
    def create(self, validated_data):
        password = validated_data['password']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user