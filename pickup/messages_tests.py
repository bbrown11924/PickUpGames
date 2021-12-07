from django.test import TestCase
from pickup.models import Player
from pickup.models import Messages
from django.urls import reverse


class MessageModelTests(TestCase):

    def test_message_exists(self):
        player1 = Player.objects.create_user("prof", "prof@umbc.edu", "cats")
        player1.save()
        player2 = Player.objects.create_user("student", "student@umbc.edu", "project")
        player2.save()
        user_message = Messages.objects.create(sender=player1, receiver=player2,
                                               message="Dont forget to commit when theres no errors!")
        user_message.save()
        self.assertEqual(Messages.objects.get(sender=player1), Messages.objects.get(receiver=player2))


class MessageViewTest(TestCase):

    # Test that the messages page can be reached when signed in
    def test_message_page_exists(self):
        player = Player.objects.create_user("test", "test@test.test", "test")
        player.save()
        fields = {"username": "test", "password": "test"}
        self.client.post(reverse("login"), fields)

        response = self.client.get(reverse("messages"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Conversation")

    # Tests that redirect works when user not signed in
    def test_message_page_redirect(self):
        response = self.client.get(reverse("messages"))
        self.assertRedirects(response, reverse("login") + "?next=" +
                             reverse("messages"))

    # Tests that default message appears when user has no conversations
    def test_no_conversation_list(self):
        player = Player.objects.create_user("test", "test@test.test", "test")
        player.save()
        fields = {"username": "test", "password": "test"}
        self.client.post(reverse("login"), fields)

        response = self.client.get(reverse("messages"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Conversations")

    # Tests that username comes up in conversation sidebar
    def test_conversation_list(self):
        player = Player.objects.create_user("test", "test@test.test", "test")
        player.save()
        fields = {"username": "test", "password": "test"}
        self.client.post(reverse("login"), fields)

        player2 = Player.objects.create_user("test2", "test2@test.test", "test2")
        player2.save()

        user_message = Messages.objects.create(sender=player, receiver=player2,
                                               message="This is a test")
        user_message.save()

        response = self.client.get(reverse("messages"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test2")

    # Tests that user messages will appear on conversation page
    def test_messages_page(self):
        player = Player.objects.create_user("test", "test@test.test", "test")
        player.save()
        fields = {"username": "test", "password": "test"}
        self.client.post(reverse("login"), fields)

        player2 = Player.objects.create_user("test2", "test2@test.test", "test2")
        player2.save()

        user_message = Messages.objects.create(sender=player, receiver=player2,
                                               message="Can you see me?")
        user_message.save()

        response = self.client.get(reverse("messages_conversation", kwargs={'username': 'test2'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Can you see me?")


class NewConversationsView(TestCase):
    # Test that the new message page can be reached when signed in
    def test_message_page_exists(self):
        player = Player.objects.create_user("test", "test@test.test", "test")
        player.save()
        fields = {"username": "test", "password": "test"}
        self.client.post(reverse("login"), fields)

        response = self.client.get(reverse("new_message"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Player's Username")

    # Tests that redirect works when user not signed in
    def test_message_page_redirect(self):
        response = self.client.get(reverse("new_message"))
        self.assertRedirects(response, reverse("login") + "?next=" +
                             reverse("new_message"))

