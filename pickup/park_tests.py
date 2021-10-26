from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from pickup.models import Parks

# tests for the Player model, independent of any view
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
        response = self.client.get(reverse('Add Park'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add New Park")