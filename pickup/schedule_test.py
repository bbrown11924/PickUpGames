from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from pickup.models import Schedule, Player, Parks
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

        new_entry = Schedule(player=my_user, park=park, date='2023-11-03',time='4')
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
            new_entry = Schedule(player=my_user, park=park, date='7', time='4')
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
        response = self.client.get(reverse('park_signup',  kwargs={'parkid': park.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Schedule Time for Parky")

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

        fields = {'date': '2024-11-04', 'time': '4'}
        response = self.client.post(reverse('park_signup',  kwargs={'parkid': park.id}), fields)

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

        fields = {'date': '2020-11-04', 'time': '4'}
        response = self.client.post(reverse('park_signup',  kwargs={'parkid': park.id}), fields)

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

        fields = {'date': '2024-11-05', 'time': '4'}
        self.client.post(reverse('park_signup', kwargs={'parkid': park.id}), fields)
        response = self.client.post(reverse('park_signup',  kwargs={'parkid': park.id}), fields)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Already signed up for this slot")
        self.assertContains(response, "Nov. 5, 2024")

