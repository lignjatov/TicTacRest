from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class TicTacToeGame(models.Model):
    class GameState(models.TextChoices):
        WAITING = 'Awaiting', _('Waiting on players'),
        IN_PROGRESS = 'Progress', _('Game in progress')
        FINISHED = 'Finished', _('Finshed game')
    creation_time = models.DateTimeField(auto_now_add=True)
    game_state = models.CharField(max_length=8, choices=GameState.choices, default=GameState.WAITING)
    creator = models.ForeignKey(User, related_name="created_games", on_delete=models.CASCADE)
    opponent = models.ForeignKey(User, related_name="participated_games", on_delete=models.SET_NULL, null=True, default=None)
    game_board = models.CharField(max_length=9, default="---------")
    winner = models.ForeignKey(User, related_name="winner", on_delete=models.SET_NULL, null=True, default=None)
    #Depending on the state of the boolean, if False, it is the room creators turn
    #else it will be the opponents turn
    player_turn = models.BooleanField(default=False)
    