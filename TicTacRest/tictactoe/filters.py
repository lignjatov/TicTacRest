from django_filters.rest_framework import FilterSet
import django_filters
from tictactoe.models import TicTacToeGame

class GameFilter(FilterSet):
    creator_filter = django_filters.CharFilter(field_name='creator__username', lookup_expr='icontains')
    opponent_filter = django_filters.CharFilter(field_name='opponent__username', lookup_expr='icontains')
    winner_filter = django_filters.CharFilter(field_name='winner__username', lookup_expr='icontains')
    before_date = django_filters.IsoDateTimeFilter(field_name='creation_time', lookup_expr='date__lt')
    after_date = django_filters.IsoDateTimeFilter(field_name='creation_time', lookup_expr='date__gt')

    class Meta:
        model = TicTacToeGame
        fields = ['creator_filter', 'opponent_filter', 'winner_filter', 'before_date', 'after_date', 'game_state']