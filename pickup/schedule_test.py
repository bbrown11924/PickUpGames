from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from pickup.models import Schedule, Player, Parks

# tests for the Schedule model, independent of any view
class ScheduleModelTests(TestCase):

    # test adding a new Entry
    def test_add_schedule_entry(self):
        my_user = User.objects.create(username='Testuser')

        new_entry = Schedule(player=my_user, date='2023-11-03',time='4')
        new_entry.save()

        entry = Schedule.objects.get(date='2023-11-03')
        self.assertEqual(entry.date, '2023-11-03')

    # test adding an entry with a past time
    def test_add_past_date(self):
        my_user = User.objects.create(username='Testuser')

        try:
            new_entry = Schedule(player=my_user, date='2020-11-03', time='4')
            new_entry.save()
        except IntegrityError:
            return
        self.assertEqual(0, 1)

class ScheduleViewTests(TestCase):
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
        print(reverse('park_signup',  kwargs={'parkid': park.id}))
        response = self.client.get(reverse('park_signup',  kwargs={'parkid': park.id}))

        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "Schedule Time for Parky")