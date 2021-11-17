from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from pickup.models import Schedule, Player, Parks, EventSignup
import datetime

# tests for the Schedule model, independent of any view
class ScheduleModelTests(TestCase):

    # test adding a new Entry
    def test_add_schedule_entry(self):
        my_user = User.objects.create(username='Testuser')

        new_park = Parks(player=my_user, name='Parky',
                         street='Parkstreet', city='Parkville',
                         state='AZ', zipcode='12345')
        new_park.save()

        park = Parks.objects.get(name="Parky")

        new_entry = Schedule(creator=my_user, park=park, date='2023-11-03',time='4')
        new_entry.save()

        entry = Schedule.objects.get(date='2023-11-03')
        self.assertEqual(entry.date, datetime.date(2023, 11, 3))

    # test adding an entry with a past time
    def test_add_bad_date(self):
        my_user = User.objects.create(username='Testuser')

        new_park = Parks(player=my_user, name='Parky',
                         street='Parkstreet', city='Parkville',
                         state='AZ', zipcode='12345')
        new_park.save()

        park = Parks.objects.get(name="Parky")

        try:
            new_entry = Schedule(creator=my_user, park=park, date='7', time='4')
            new_entry.save()
        except Exception:
            return
        self.assertEqual(0, 1)

class ScheduleViewTests(TransactionTestCase):
    def test_schedule_page_exists(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()

        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        new_park = Parks(player=player, name='Parky',
                         street='Parkstreet', city='Parkville',
                         state='AZ', zipcode='12345')
        new_park.save()

        park = Parks.objects.get(name="Parky")
        response = self.client.get(reverse('event_signup',  kwargs={'parkid': park.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Schedule at Parky")

    def test_schedule_add(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()

        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        new_park = Parks(player=player, name='Parky',
                         street='Parkstreet', city='Parkville',
                         state='AZ', zipcode='12345')
        new_park.save()

        park = Parks.objects.get(name="Parky")

        fields = {'date': '2024-11-04', 'time': '4', 'name': 'Test Match'}
        response = self.client.post(reverse('event_signup',  kwargs={'parkid': park.id}), fields)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nov. 4, 2024")

    def test_schedule_add_past_date(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()

        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        new_park = Parks(player=player, name='Parky',
                         street='Parkstreet', city='Parkville',
                         state='AZ', zipcode='12345')
        new_park.save()

        park = Parks.objects.get(name="Parky")

        fields = {'date': '2020-11-04', 'time': '4', 'name': 'Test Match'}
        response = self.client.post(reverse('event_signup',  kwargs={'parkid': park.id}), fields)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The date cannot be in the past!")
        self.assertNotContains(response, "Nov. 4, 2020")

    def test_schedule_add_duplicate(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()

        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        new_park = Parks(player=player, name='Parky',
                         street='Parkstreet', city='Parkville',
                         state='AZ', zipcode='12345')
        new_park.save()

        park = Parks.objects.get(name="Parky")

        fields = {'date': '2024-11-05', 'time': '4', 'name': 'Test Match'}
        self.client.post(reverse('event_signup', kwargs={'parkid': park.id}), fields)
        response = self.client.post(reverse('event_signup',  kwargs={'parkid': park.id}), fields)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is already a match at this time with this name")
        self.assertContains(response, "Nov. 5, 2024")

class JoiningEventTests(TransactionTestCase):

    def test_join_and_leave_event(self):

        my_user = User.objects.create(username='Testuser')

        # create some parks
        new_park = Parks(player=my_user, name='Yosemite',
                          street='Bear', city='Parkville',
                          state='CA', zipcode='12378')

        new_park.save()

        # log in
        user = Player.objects.create_user("Chevy", "corvette@c6.org",
                                          "fa5test")
        user.save()

        # log in and get the parks page
        fields = {"username": "Chevy", "password": "fa5test"}
        response = self.client.post(reverse("login"), fields)


        # Load page and check events
        park = Parks.objects.get(name='Yosemite').id
        response = self.client.get(reverse("event_signup", kwargs={'parkid':park}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Schedule at Yosemite")
        self.assertNotContains(response, "My Matches")
        self.assertNotContains(response, "Other Matches")

        #Create a test match
        fields = {'date': '2024-11-05', 'time': '4', 'name': 'Test Match'}
        self.client.post(reverse('event_signup', kwargs={'parkid': park}), fields)

        #Get the test match id and join the match
        eventid = Schedule.objects.get(name='Test Match').id
        fields = {'parkid':park, 'add':1, 'eventid':eventid}
        self.client.post(reverse("join_event", kwargs=fields), fields)

        #See that the my matches section comes up, showing that it was added
        response = self.client.get(reverse("event_signup", kwargs={'parkid': park}))
        self.assertContains(response, "Schedule at Yosemite")
        self.assertContains(response, "My Matches")
        self.assertNotContains(response, "Other Matches")

        #Leave the match
        fields = {'parkid': park, 'add': 0, 'eventid': eventid}
        self.client.post(reverse("join_event", kwargs=fields), fields)

        # See that the other matches section appears, showing that you left the match
        response = self.client.get(reverse("event_signup", kwargs={'parkid': park}))
        self.assertContains(response, "Schedule at Yosemite")
        self.assertNotContains(response, "My Matches")
        self.assertContains(response, "Other Matches")

    def test_join_player_view(self):
        my_user = User.objects.create(username='Testuser')

        # create some parks
        new_park = Parks(player=my_user, name='Yosemite',
                         street='Bear', city='Parkville',
                         state='CA', zipcode='12378')

        new_park.save()

        # log in
        user = Player.objects.create_user("Chevy", "corvette@c6.org",
                                          "fa5test")
        user.first_name = "Chevy"
        user.last_name = "Corvette"
        user.save()

        # log in and get the parks page
        fields = {"username": "Chevy", "password": "fa5test"}
        response = self.client.post(reverse("login"), fields)

        # Load page and check events
        park = Parks.objects.get(name='Yosemite').id
        response = self.client.get(reverse("event_signup", kwargs={'parkid': park}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Schedule at Yosemite")
        self.assertNotContains(response, "My Matches")
        self.assertNotContains(response, "Other Matches")

        # Create a test match
        fields = {'date': '2024-11-05', 'time': '4', 'name': 'Test Match'}
        self.client.post(reverse('event_signup', kwargs={'parkid': park}), fields)

        # Get the test match id and join the match
        eventid = Schedule.objects.get(name='Test Match').id
        fields = {'parkid': park, 'add': 1, 'eventid': eventid}
        self.client.post(reverse("join_event", kwargs=fields), fields)

        #Up to this point we have created a match and joined it.  Now we should be
        #able to look at the join/leave page and see if it has all the information
        response = self.client.get(reverse("join_event", kwargs=fields))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chevy Corvette")
        self.assertContains(response, "Test Match")
        self.assertContains(response, "Join this match?")

    def test_join_match_twice(self):
        my_user = User.objects.create(username='Testuser')

        # create some parks
        new_park = Parks(player=my_user, name='Yosemite',
                         street='Bear', city='Parkville',
                         state='CA', zipcode='12378')

        new_park.save()

        # log in
        user = Player.objects.create_user("Chevy", "corvette@c6.org",
                                          "fa5test")
        user.first_name = "Chevy"
        user.last_name = "Corvette"
        user.save()

        # log in and get the parks page
        fields = {"username": "Chevy", "password": "fa5test"}
        response = self.client.post(reverse("login"), fields)

        # Load page and check events
        park = Parks.objects.get(name='Yosemite').id
        response = self.client.get(reverse("event_signup", kwargs={'parkid': park}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Schedule at Yosemite")
        self.assertNotContains(response, "My Matches")
        self.assertNotContains(response, "Other Matches")

        # Create a test match
        fields = {'date': '2024-11-05', 'time': '4', 'name': 'Test Match'}
        self.client.post(reverse('event_signup', kwargs={'parkid': park}), fields)

        # Get the test match id and join the match
        eventid = Schedule.objects.get(name='Test Match').id
        fields = {'parkid': park, 'add': 1, 'eventid': eventid}
        self.client.post(reverse("join_event", kwargs=fields), fields)
        response = self.client.post(reverse("join_event", kwargs=fields), fields)

        #Ensure that the error message pops up
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error: You have already joined this match!")

