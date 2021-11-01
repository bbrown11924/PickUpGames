from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from models import Player
from models import Messages

class messaging_tests(TestCase):

    def test_send(self):
        player1 = Player.objects.create_user("prof", "prof@umbc.edu", "cats")
        player1.save()
        player2 = Player.objects.create_user("student", "student@umbc.edu", "project")
        player2.save()

