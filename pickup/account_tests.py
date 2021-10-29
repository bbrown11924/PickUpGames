# File: account_tests.py
# Author: Josh Galita
#
# This file contains tests pertaining to account information. This includes
# registering for a new account, logging into an existing account, and
# modifying profile information

import datetime

from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.utils import timezone

from .models import Player

# tests for account registration
class RegistrationTests(TestCase):

    # test to make sure the registration page can be accessed
    def test_register_page_exists(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Account")

    # test to make sure an error message is printed when the password and
    # confirm password boxes do not match
    def test_mismatched_passwords(self):
        fields = {"username": "rbg",
                  "email": "rbg@supremecourt.gov",
                  "password": "N0torious",
                  "confirm_password": "Notor1ous"}
        response = self.client.post(reverse("register"), fields)

        # check for error message and form redisplay
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Account")
        self.assertContains(response, "Error: Passwords do not match.")

        # check for username and email boxes still filled
        self.assertContains(response, "rbg")
        self.assertContains(response, "rbg@supremecourt.gov")

    # test to make sure an error message whenever an improperly formatted email
    # is given
    def test_bad_email(self):
        fields = {"username": "Cat",
                  "email": "cat.has.bad.email",
                  "password": "Il0ved0gs!",
                  "confirm_password": "Il0ved0gs!"}
        response = self.client.post(reverse("register"), fields)

        # check for error message and form redisplay
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Account")
        self.assertContains(response, "Error: Invalid email address.")

        # check for username box filled, but not email box
        self.assertContains(response, "Cat")
        self.assertNotContains(response, "cat.has.bad.email")

    # test to ensure an error message is printed if no user name is given
    def test_no_username(self):
        fields = {"username": "",
                  "email": "potus@whitehouse.gov",
                  "password": "Biden2024",
                  "confirm_password": "Biden2024"}
        response = self.client.post(reverse("register"), fields)

        # check for error message and form redisplay
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Account")
        self.assertContains(response, "Error: All fields are required.")

    # test to ensure an error message is printed if no email is given
    def test_no_email(self):
        fields = {"username": "Joe",
                  "email": "",
                  "password": "Biden2024",
                  "confirm_password": "Biden2024"}
        response = self.client.post(reverse("register"), fields)

        # check for error message and form redisplay
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Account")
        self.assertContains(response, "Error: All fields are required.")

    # test to ensure an error message is printed if the password field is blank
    def test_no_password(self):
        fields = {"username": "Joe",
                  "email": "potus@whitehouse.gov",
                  "password": "",
                  "confirm_password": "Biden2024"}
        response = self.client.post(reverse("register"), fields)

        # check for error message and form redisplay
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Account")
        self.assertContains(response, "Error: All fields are required.")

    # test to ensure an error message is printed if the confirm_password field is
    # blank
    def test_no_confirm_password(self):
        fields = {"username": "Joe",
                  "email": "potus@whitehouse.gov",
                  "password": "Biden2024",
                  "confirm_password": ""}
        response = self.client.post(reverse("register"), fields)

        # check for error message and form redisplay
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Account")
        self.assertContains(response, "Error: All fields are required.")

    # test to make sure a valid user is successfully added
    def test_register_player(self):
        fields = {"username": "ProfJ",
                  "email": "ben.johnson@umbc.edu",
                  "password": "TestAsYouGo!",
                  "confirm_password": "TestAsYouGo!"}
        response = self.client.post(reverse("register"), fields)

        # check for success
        self.assertRedirects(response, reverse("view_profile"))
        prof = Player.objects.get(username="ProfJ")
        self.assertEqual(prof.email, "ben.johnson@umbc.edu")

    # test to ensure two users with the same username cannot be added
    def test_register_duplicate_usernames(self):
        player1 = Player.objects.create_user("Joe", "biden@whitehouse.gov",
                                             "Delaware!")
        player1.save()

        fields = {"username": "Joe",
                  "email": "manchin@senate.gov",
                  "password": "C0ALcountry",
                  "confirm_password": "C0ALcountry"}
        response = self.client.post(reverse("register"), fields)

        # check for error message and form redisplay with username box blank
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Account")
        self.assertContains(response, "Error: User name unavailable.")
        self.assertNotContains(response, "Joe")


# tests for the Player model, independent of any view
class PlayerModelTests(TestCase):

    # test adding a new player
    def test_add_player(self):
        new_player = Player.objects.create_user("Kamala", "vp@whitehouse.gov",
                                                "Harris2024")
        new_player.save()
        vp = Player.objects.get(username="Kamala")
        self.assertEqual(vp, new_player)

    # test adding 2 players with the same username
    def test_duplicate_usernames(self):
        player1 = Player.objects.create_user("Joe", "biden@whitehouse.gov",
                                             "Delaware!")
        player1.save()

        # make sure an IntegrityError is raised for a second "Joe"
        try:
            player2 = Player.objects.create_user("Joe", "manchin@senate.gov",
                                                 "CoalIsC00l")
        except IntegrityError:
            return
        self.assertEqual(0, 1)

    # test getting a player's age using the get_age() function
    def test_get_age(self):
        player = Player.objects.create_user("Albert", "einstein@umbc.edu",
                                            "RelativisticAge")
        player.save()
        bday = timezone.now()

        # loop over last 80 years in increments of 5
        for i in range(0, 85, 5):
            player.date_of_birth = bday - datetime.timedelta(days=366*i)
            player.save()
            self.assertEqual(player.get_age(), i)

    # test getting a player's age using the get_age() function when no date of
    # birth is given
    def test_get_age_without_date_of_birth(self):
        player = Player.objects.create_user("God", "him@heaven.org",
                                            "0ldAsTime")
        player.save()
        self.assertEqual(player.get_age(), None)

    # test getting the string for a user's gender
    def test_get_gender(self):
        player = Player.objects.create_user("AOC", "ocasiocortez@house.gov",
                                            "%TaxTheRich%")
        player.gender = Player.FEMALE
        player.save()
        
        read_player = Player.objects.get(username="AOC")
        self.assertEqual(read_player.get_gender_display(), "Female")


# tests for account login
class LoginTests(TestCase):

    # test logging in a user and viewing their profile
    def test_login_user(self):
        player = Player.objects.create_user("npelosi", "speaker@house.gov",
                                            "HouseDems")
        player.save()

        fields = {"username": "npelosi", "password": "HouseDems"}
        response = self.client.post(reverse("login"), fields)

        # verify successful redirect
        self.assertRedirects(response, reverse("view_profile"))

        # verify profile page can be accessed
        response = self.client.get(reverse("view_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Profile")

    # test accessing the profile page without logging in
    def test_access_profile_without_login(self):
        response = self.client.get(reverse("view_profile"))
        self.assertRedirects(response, reverse("login") + "?next=" +
                                       reverse("view_profile"))

    # test logging in a user that does not exist
    def test_login_unknown_user(self):
        fields = {"username": "independent", "password": "M0derate?"}
        response = self.client.post(reverse("login"), fields)

        # check for login page redisplay with error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Error: Invalid login credentials.")

    # test logging with the wrong password
    def test_login_with_wrong_password(self):
        player = Player.objects.create_user("kmccarthy", "gopleader@house.gov",
                                            "HouseGOP")
        player.save()

        fields = {"username": "kmccarthy", "password": "HouseG0P"}
        response = self.client.post(reverse("login"), fields)

        # check for login page redisplay with error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Error: Invalid login credentials.")

    # test logging in then logging out
    def test_login_then_logout(self):
        player = Player.objects.create_user("BenJohnson",
                                            "ben.johnson@umbc.edu",
                                            "Cats4ever")
        player.save()

        # log in
        fields = {"username": "BenJohnson", "password": "Cats4ever"}
        response = self.client.post(reverse("login"), fields)
        self.assertRedirects(response, reverse("view_profile"))

        # log out
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

        # ensure we are logged out
        response = self.client.get(reverse("view_profile"))
        self.assertRedirects(response, reverse("login") + "?next=" +
                                       reverse("view_profile"))
