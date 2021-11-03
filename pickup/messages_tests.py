from django.test import TestCase
from pickup.models import Player
from pickup.models import Messages


class messaging_tests(TestCase):

    def test_message_exists(self):
        player1 = Player.objects.create_user("prof", "prof@umbc.edu", "cats")
        player1.save()
        player2 = Player.objects.create_user("student", "student@umbc.edu", "project")
        player2.save()
        user_message = Messages.objects.create(sender= player1, reciever= player2, message= "Dont forget to commit when theres no errors!")
        user_message.save()
        self.assertEqual(Messages.objects.get(sender=player1), user_message)
