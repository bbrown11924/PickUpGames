from .models import Profile, Player, Parks, Schedule, EventSignup

from pickup.navbar_tests import *

from pickup.account_tests import *
from pickup.park_tests import *
from pickup.messages_tests import *
from pickup.schedule_test import *


# Test cases to make sure that pages exist
class PageExistenceTests(TestCase):

    def test_admin_page_exists(self):
        """
        Makes sure the admin page can be accessed
        """
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)


# tests for the page at the root url
class IndexPageTests(TestCase):
    def test_index_page_exists(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # test accessing the index page without logging in
    def test_index_page_without_login(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Login")
        self.assertContains(response, "Who Are We?")
        self.assertNotContains(response, "Your Dashboard")
        self.assertNotContains(response, "Your Signups")

    # test accessing the index page while logged in
    def test_index_page_with_login(self):
        player = Player.objects.create_user("Chief", "roberts@supremecourt.gov",
                                            "Justice4Life")

        # log in and go to the index page page
        fields = {"username": "Chief", "password": "Justice4Life"}
        response = self.client.post(reverse("login"), fields)
        response = self.client.get(reverse('index'))

        self.assertNotContains(response, "Login")
        self.assertNotContains(response, "Who Are We?")
        self.assertContains(response, "Your Dashboard")
        self.assertContains(response, "Your Signups")

        # verify that there are no signups for this player
        self.assertContains(response,
                            "You haven't signed up for any matches yet!")

    # test viewing a signup on the home page
    def test_view_signup_on_home_page(self):

        # create a player, park, match, and signup
        player = Player.objects.create_user("Chief", "roberts@supremecourt.gov",
                                            "Justice4Life")
        player.save()

        park = Parks(player=player, name='Supreme Court',
                     street='1 First St NE', city='Washington',
                     state='DC', zipcode='20543')
        park.save()

        match = Schedule(name="Justices Only Game", creator=player, park=park,
                         date="2021-12-01", time=40)
        match.save()

        signup = EventSignup(player=player, event=match)
        signup.save()

        # log in and go to the index page page
        fields = {"username": "Chief", "password": "Justice4Life"}
        response = self.client.post(reverse("login"), fields)
        response = self.client.get(reverse('index'))

        # verify that the signup appears
        self.assertContains(response, "Justices Only Game")
        self.assertContains(response, "Dec. 1, 2021 at 10:00 AM")
        self.assertContains(response, "Supreme Court")
        self.assertContains(response, "1 First St NE")
        self.assertContains(response, "Washington, DC")
        self.assertContains(response, "20543")
        self.assertNotContains(response,
                            "You haven't signed up for any matches yet!")


class DatabaseTests(TestCase):

    def test_height_string_functionality(self):
        # Insert an element into the profile database
        q = Profile(name="Benjamin", weight = 160, height = 67)
        q.save()
        #Check if the proper height string is returned
        self.assertIs('5\'7\"' == q.get_height_cust(), True)
