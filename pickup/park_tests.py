from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from pickup.models import Parks, Player

# tests for the Park model, independent of any view
class ParkModelTests(TestCase):

    # test adding a new Park
    def test_add_park(self):
        my_user = User.objects.create(username='Testuser')

        new_park = Parks(player=my_user, name='Parky',
                         street='Parkstreet', city='Parkville',
                         state='AZ', zipcode='12345')
        new_park.save()

        park = Parks.objects.get(name="Parky")
        self.assertEqual(park.name, 'Parky')

    # test adding 2 parks with the same information
    def test_duplicate_parks(self):
        my_user = User.objects.create(username='Testuser')

        new_park = Parks(player=my_user, name='Parky',
                         street='Parkstreet', city='Parkville',
                         state='AZ', zipcode='12345')
        new_park.save()

        # make sure an IntegrityError is raised for a second park
        try:
            dup_park = Parks(player=my_user, name='Parky',
                             street='Parkstreet', city='Parkville',
                             state='AZ', zipcode='12345')
            dup_park.save()
        except IntegrityError:
            return
        self.assertEqual(0, 1)


#Park has been added!
class ParkViewTests(TestCase):

    def test_add_park_page_exists(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()
        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        response = self.client.get(reverse('Add Park'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add New Park")

    # test accessing the add park page without logging in
    def test_access_profile_without_login(self):
        response = self.client.get(reverse("view_profile"))
        self.assertRedirects(response, reverse("login") + "?next=" +
                             reverse("view_profile"))

    def test_add_park_invalid_zip(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()
        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        fields = {'name':'Parky', 'street':'Parkstreet', 'city':'Parkville',
                             'state':'AZ', 'zipcode':'123456'}
        response = self.client.post(reverse('Add Park'), fields)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a zip code in the format")
        self.assertNotContains(response, "Park has been added!")

    def test_add_park_missing_info(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()
        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        fields = {'name':'Parky', 'street':'Parkstreet', 'city':'',
                             'state':'AZ', 'zipcode':'12345'}
        response = self.client.post(reverse('Add Park'), fields)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Park has been added!")

    def test_add_park_bad_state(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()
        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        fields = {'name':'Parky', 'street':'Parkstreet', 'city':'Parkville',
                             'state':'BS', 'zipcode':'12345'}
        response = self.client.post(reverse('Add Park'), fields)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Park has been added!")

    def test_add_park_good(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()
        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        fields = {'name':'Good Park', 'street':'Parkstreet', 'city':'Parkville',
                             'state':'MD', 'zipcode':'12345'}
        response = self.client.post(reverse('Add Park'), fields)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Park has been added!")

        park = Parks.objects.get(name="Good Park")
        self.assertEqual(park.name, 'Good Park')