# File: account_tests.py
# Author: Josh Galita
#
# This file contains tests pertaining to account information. This includes
# registering for a new account, logging into an existing account, and
# modifying profile information

import datetime
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.utils import timezone

from pickup.models import Player

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
        self.assertRedirects(response, reverse("edit_profile"))
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
        bday = datetime.datetime.now()

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

    # test logging in and redirecting to the edit profile page
    def test_login_the_redirect_to_edit_profile(self):
        player = Player.objects.create_user("BenJohnson",
                                            "ben.johnson@umbc.edu",
                                            "Cats4ever")
        player.save()

        # log in
        fields = {"username": "BenJohnson", "password": "Cats4ever"}
        response = self.client.post(reverse("login") + "?next=" +
                                    reverse("edit_profile"), fields)
        self.assertRedirects(response, reverse("edit_profile"))


# tests for viewing and editing the profile page
class ProfileTests(TestCase):

    # test viewing a profile
    def test_view_profile(self):
        player = Player.objects.create_user("44", "barack@obama.org",
                                            "YesWeCan!")
        player.first_name = "Barack"
        player.last_name = "Obama"
        player.date_of_birth = datetime.date(1961, 8, 4)
        player.gender = Player.MALE
        player.height = 74
        player.weight = 175
        player.save()

        # log in and go to profile page
        fields = {"username": "44", "password": "YesWeCan!"}
        response = self.client.post(reverse("login"), fields)
        self.assertRedirects(response, reverse("view_profile"))
        response = self.client.get(reverse("view_profile"))

        # check for correct information
        self.assertContains(response, "Your Profile")
        self.assertContains(response, "44")
        self.assertContains(response, "Barack Obama")
        age = player.get_age()
        self.assertContains(response, age)
        self.assertContains(response, "Male")
        self.assertContains(response, "74 in")
        self.assertContains(response, "175 lbs")
        self.assertContains(response, "Edit Profile")

    # test that the edit profile page contains information already filled in
    def test_edit_profile_autofill(self):
        player = Player.objects.create_user("44", "barack@obama.org",
                                            "YesWeCan!")
        player.first_name = "Barack"
        player.last_name = "Obama"
        player.date_of_birth = datetime.date(1961, 8, 4)
        player.gender = Player.MALE
        player.height = 74
        player.weight = 175
        player.save()

        # log in
        fields = {"username": "44", "password": "YesWeCan!"}
        response = self.client.post(reverse("login"), fields)

        # get the edit profile page and check for correct information
        response = self.client.get(reverse("edit_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "44")
        self.assertContains(response, "Barack")
        self.assertContains(response, "Obama")
        self.assertContains(response, "1961-08-04")
        self.assertContains(response, "Male")
        self.assertContains(response, "74")
        self.assertContains(response, "175")

    # test filling out the edit page and viewing the profile page afterwards
    def test_edit_then_view_profile(self):
        player = Player.objects.create_user("RBG", "ginsburg@supremecourt.gov",
                                            "FightingFor=")
        player.save()

        # log in
        fields = {"username": "RBG", "password": "FightingFor="}
        response = self.client.post(reverse("login"), fields)

        # go to the edit profile page and fill in info
        response = self.client.get(reverse("edit_profile"))
        fields = {"first_name": "Ruth",
                  "last_name": "Bader Ginsburg",
                  "date_of_birth": "1933-03-15",
                  "gender": Player.FEMALE,
                  "height": "61",
                  "weight": "110"}
        response = self.client.post(reverse("edit_profile"), fields)
        self.assertRedirects(response, reverse("view_profile"))

        # get the profile page results
        response = self.client.get(reverse("view_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Profile")
        self.assertContains(response, "RBG")
        self.assertContains(response, "Ruth Bader Ginsburg")
        age = relativedelta(datetime.date.today(),
                            datetime.date(1933, 3, 15)).years
        self.assertContains(response, age)
        self.assertContains(response, "Female")
        self.assertContains(response, "61 in")
        self.assertContains(response, "110 lbs")


# tests for changing a user's password
class ChangePasswordTests(TestCase):

    # try to access the change password page without logging in
    def get_change_password_page_without_login(self):
        response = self.client.get(reverse("change_password"))
        self.assertRedirects(response, reverse("login"))

    # test filling out the filling out the change password page, logging out,
    # and logging back in with both the old and new passwords
    def test_change_password(self):
        player = Player.objects.create_user("Ted", "cruz@senate.gov",
                                            "ObamaIsTheWorst!")
        player.save()

        # log in
        fields = {"username": "Ted", "password": "ObamaIsTheWorst!"}
        response = self.client.post(reverse("login"), fields)

        # go to the change password page
        response = self.client.get(reverse("change_password"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Change Password")

        # change the user's password
        fields = {"old_password": "ObamaIsTheWorst!",
                  "new_password": "BidenIsTheWorst!",
                  "confirm_password": "BidenIsTheWorst!",}
        response = self.client.post(reverse("change_password"), fields)
        self.assertRedirects(response, reverse("view_profile"))

        # log out
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

        # try logging in with the old password
        fields = {"username": "Ted", "password": "ObamaIsTheWorst!"}
        response = self.client.post(reverse("login"), fields)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error: Invalid login credentials.")

        # try logging in with the new password
        fields = {"username": "Ted", "password": "BidenIsTheWorst!"}
        response = self.client.post(reverse("login"), fields)
        self.assertEqual(response.status_code, 302)

    # test trying to change the user's password with the wrong old password
    def test_change_password_with_wrong_old_password(self):
        player = Player.objects.create_user("Mitch", "GopLeader@senate.gov",
                                            "NotTrump2016")
        player.save()

        # log in
        fields = {"username": "Mitch", "password": "NotTrump2016"}
        response = self.client.post(reverse("login"), fields)

        # try changing the user's password
        fields = {"old_password": "Trump2016",
                  "new_password": "Trump2020",
                  "confirm_password": "Trump2020",}
        response = self.client.post(reverse("change_password"), fields)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error: Incorrect old password.")

    # test trying to change the user's password with a different new password
    # and confirmed password
    def test_change_password_with_mismatched_passwords(self):
        player = Player.objects.create_user("Mitch", "GopLeader@senate.gov",
                                            "LowerTaxes!")
        player.save()

        # log in
        fields = {"username": "Mitch", "password": "LowerTaxes!"}
        response = self.client.post(reverse("login"), fields)

        # try changing the user's password
        fields = {"old_password": "LowerTaxes!",
                  "new_password": "LowerSpending!",
                  "confirm_password": "LowerDemocraticSpending!",}
        response = self.client.post(reverse("change_password"), fields)

        self.assertEqual(response.status_code, 200)
        error_string = "Error: New password does not match confirmed password."
        self.assertContains(response, error_string)


# tests for viewing any player's profile
class ViewPlayerTests(TestCase):

    # test viewing one's own profile through the player viewing interface
    def test_view_player_self(self):
        player = Player.objects.create_user("DrFauci", "fauci@niaid.nih.gov",
                                            "Vaccinated.")
        player.first_name = "Anthony"
        player.last_name = "Fauci"
        player.date_of_birth = datetime.date(1940, 12, 24)
        player.gender = Player.MALE
        player.height = 67
        player.weight = 176
        player.save()

        # log in and go to player/DrFauci page
        fields = {"username": "DrFauci", "password": "Vaccinated."}
        response = self.client.post(reverse("login"), fields)
        response = self.client.get(reverse("view_player", args=["DrFauci"]))

        # check for correct information
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Profile")
        self.assertContains(response, "DrFauci")
        self.assertContains(response, "Anthony Fauci")
        age = player.get_age()
        self.assertContains(response, age)
        self.assertContains(response, "Male")
        self.assertContains(response, "67 in")
        self.assertContains(response, "176 lbs")
        self.assertContains(response, "Edit Profile")

    # test viewing another player's profile
    def test_view_other_player(self):
        user = Player.objects.create_user("DrFauci", "fauci@niaid.nih.gov",
                                          "Vaccinated.")

        player = Player.objects.create_user("CDC_Director", "walensky@cdc.gov",
                                            "EndCOVID!")
        player.first_name = "Rochelle"
        player.last_name = "Walensky"
        player.date_of_birth = datetime.date(1969, 4, 5)
        player.gender = Player.FEMALE
        player.height = 71
        player.weight = 137
        player.save()

        # log in and go to player/CDC_Director page
        fields = {"username": "DrFauci", "password": "Vaccinated."}
        response = self.client.post(reverse("login"), fields)
        response = self.client.get(reverse("view_player",
                                           args=["CDC_Director"]))

        # check for correct information
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Player Profile")
        self.assertContains(response, "CDC_Director")
        self.assertContains(response, "Rochelle Walensky")
        age = player.get_age()
        self.assertContains(response, age)
        self.assertContains(response, "Female")
        self.assertContains(response, "71 in")
        self.assertContains(response, "137 lbs")
        self.assertNotContains(response, "Edit Profile")




