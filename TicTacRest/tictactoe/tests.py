from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, APIClient
from tictactoe.models import User
from rest_framework.test import force_authenticate
from tictactoe.models import TicTacToeGame
import time
# Create your tests here.
class TicTacToe(APITestCase):
    def test_create_user(self):
        url = reverse("user-registration")
        response = self.client.post(url,{'username':'test1','password':'test1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().username, "test1")
    

class GameJoinTests(APITestCase):
    def setUp(self):
        self.creator = User.objects.create_user(username="jura", password="jura")
        self.opponent = User.objects.create_user(username="manus", password="manus")
        self.client = APIClient()
        self.game = TicTacToeGame.objects.create(creator=self.creator)

    def test_join_without_login(self):
        url = reverse("game-join", kwargs={'game_id': self.game.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_join_with_jwt(self):
        url = reverse("game-join", kwargs={'game_id': self.game.id})
        response = self.client.post(reverse('user-login'), {'username': 'manus', 'password': 'manus'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 200)


class GameMoveTests(APITestCase):
    def setUp(self):
        self.creator = User.objects.create_user(username="jura", password="jura")
        self.opponent = User.objects.create_user(username="manus", password="manus")
        self.client = APIClient()
        self.game = TicTacToeGame.objects.create(creator=self.creator, opponent=self.opponent, game_state=TicTacToeGame.GameState.IN_PROGRESS)
        
    def test_first_move_opponent(self):
        url = reverse("game-move", kwargs={'game_id': self.game.id})
        response = self.client.post(reverse('user-login'), {'username': 'manus', 'password': 'manus'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(url, data={"row":"1", "col":"1"})
        self.assertEqual(response.status_code, 403)
    
    def test_creator_move_first(self):
        url = reverse("game-move", kwargs={'game_id': self.game.id})
        response = self.client.post(reverse('user-login'), {'username': 'jura', 'password': 'jura'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(url, data={"row":"1", "col":"1"})
        self.assertEqual(response.status_code, 200)
    
    def test_move_twice(self):
        url = reverse("game-move", kwargs={'game_id': self.game.id})
        response = self.client.post(reverse('user-login'), {'username': 'jura', 'password': 'jura'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(url, data={"row":"1", "col":"1"})
        response = self.client.post(url, data={"row":"0", "col":"1"})
        self.assertEqual(response.status_code, 403)
    
    
        