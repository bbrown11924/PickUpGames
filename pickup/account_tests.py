# File: account_tests.py
# Author: Josh Galita
#
# This file contains tests pertaining to account information. This includes
# registering for a new account, logging into an existing account, and
# modifying profile information

from django.test import TestCase
from django.urls import reverse

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
        response = self.client.post(reverse("create_account"), fields)

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
        response = self.client.post(reverse("create_account"), fields)

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
        response = self.client.post(reverse("create_account"), fields)

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
        response = self.client.post(reverse("create_account"), fields)

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
        response = self.client.post(reverse("create_account"), fields)

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
        response = self.client.post(reverse("create_account"), fields)

        # check for error message and form redisplay
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Account")
        self.assertContains(response, "Error: All fields are required.")
