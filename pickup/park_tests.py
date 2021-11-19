from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from pickup.models import Parks, Player
import os

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

    # testing to see if an invalid zip format is entered
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

    # test to see if there is any crucial missing information in the address
    def test_add_park_missing_info(self):
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()
        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        fields = {'name':'Parky', 'street':'', 'city':'Parkville',
                             'state':'AZ', 'zipcode':'12345'}
        response = self.client.post(reverse('Add Park'), fields)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Park has been added!")

     # check if input state doesn't exist
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

    # checking a believable but fake address
    def test_add_park_not_real(self):
        try:
            os.environ['apiKey']
        except KeyError:
            return
            
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()
        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        fields = {'name':'Good Park', 'street':'Parkstreet', 'city':'Parkville',
                             'state':'MD', 'zipcode':'12345'}
        response = self.client.post(reverse('Add Park'), fields)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Park has been added!")


    # checking a real address
    def test_add_park_real(self):
        try:
            os.environ['apiKey']
        except KeyError:
            return
        
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()
        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        fields = {'name':'Good Park', 'street':'20 Hudson Yards', 'city':'New York',
                             'state':'NY', 'zipcode':'10001'}
        response = self.client.post(reverse('Add Park'), fields)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Park has been added!")

        park = Parks.objects.get(name="Good Park")
        self.assertEqual(park.name, 'Good Park')

    # checking a flawed real address
    def test_add_park_real_malformed_address(self):
        try:
            os.environ['apiKey']
        except KeyError:
            return
    
    
        player = Player.objects.create_user("root", "root@root.com",
                                            "root")
        player.save()
        fields = {"username": "root", "password": "root"}
        self.client.post(reverse("login"), fields)

        fields = {'name':'Good Park', 'street':'20 Huson Yards', 'city':'New York',
                             'state':'NY', 'zipcode':'10001'}
        response = self.client.post(reverse('Add Park'), fields)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Park has been added!")
        self.assertContains(response, "20 Hudson Yards, New York, NY 10001")

        
    # checking a real address
    def test_add_park_absent_apikey(self):
        try:
            os.environ['apiKey']
        except KeyError:
            player = Player.objects.create_user("root", "root@root.com",
                                            "root")
            player.save()
            fields = {"username": "root", "password": "root"}
            self.client.post(reverse("login"), fields)

            fields = {'name':'Good Park', 'street':'20 Hudson Yards', 'city':'New York',
                             'state':'NY', 'zipcode':'10001'}
            response = self.client.post(reverse('Add Park'), fields)

            self.assertEqual(response.status_code, 200)
            ###  add back in: self.assertContains(response, "The google maps api key is missing")
        return
      
        
        
# tests for searching for a player's profile
class SearchParkTests(TestCase):

    # test accessing the parks page without searching for anything
    def test_view_park_without_search(self):
        user = Player.objects.create_user("Chevy", "corvette@c6.org",
                                          "fa5test")
        user.save()

        # log in and get the parks page
        fields = {"username": "Chevy", "password": "fa5test"}
        response = self.client.post(reverse("login"), fields)

        response = self.client.get(reverse("parks"))

        # check for correct results
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search for New Parks")
        self.assertNotContains(response, "Search results")

    # test performing searches
    def test_search_parks(self):

        my_user = User.objects.create(username='Testuser')

        # create some parks
        new_park1 = Parks(player=my_user, name='Yellowstone',
                         street='Golden', city='Brickroad',
                         state='WY', zipcode='12345')
        new_park2 = Parks(player=my_user, name='Yosemite',
                          street='Bear', city='Parkville',
                          state='CA', zipcode='12378')
        new_park3 = Parks(player=my_user, name='Glacier National Park',
                          street='Cold', city='Antarctica',
                          state='MO', zipcode='54321')
        new_park1.save()
        new_park2.save()
        new_park3.save()


        # log in
        user = Player.objects.create_user("Chevy", "corvette@c6.org",
                                          "fa5test")
        user.save()

        # log in and get the parks page
        fields = {"username": "Chevy", "password": "fa5test"}
        response = self.client.post(reverse("login"), fields)


        # search with the empty string
        fields = {"search_text": ""}
        response = self.client.get(reverse("parks"), fields)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search results")
        self.assertContains(response, "Yellowstone")
        self.assertContains(response, "Yosemite")
        self.assertContains(response, "Glacier National Park")

        # search for "i"
        fields = {"search_text": "i"}
        response = self.client.get(reverse("parks"), fields)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yosemite")
        self.assertContains(response, "Glacier National Park")
        self.assertNotContains(response, "Yellowstone")

        # search for "Panda"
        fields = {"search_text": "Panda"}
        response = self.client.get(reverse("parks"), fields)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Yellowstone")
        self.assertNotContains(response, "Yosemite")
        self.assertNotContains(response, "Glacier National Park")

class FavoriteParksTests(TestCase):

    def test_favorite_and_unfavorite_parks(self):

        my_user = User.objects.create(username='Testuser')

        # create some parks
        new_park1 = Parks(player=my_user, name='Yellowstone',
                         street='Golden', city='Brickroad',
                         state='WY', zipcode='12345')
        new_park2 = Parks(player=my_user, name='Yosemite',
                          street='Bear', city='Parkville',
                          state='CA', zipcode='12378')
        new_park3 = Parks(player=my_user, name='Glacier National Park',
                          street='Cold', city='Antarctica',
                          state='MO', zipcode='54321')
        new_park1.save()
        new_park2.save()
        new_park3.save()


        # log in
        user = Player.objects.create_user("Chevy", "corvette@c6.org",
                                          "fa5test")
        user.save()

        # log in and get the parks page
        fields = {"username": "Chevy", "password": "fa5test"}
        response = self.client.post(reverse("login"), fields)


        # Load page and check favorites (will display favorites without searching)
        response = self.client.get(reverse("parks"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Search results")
        self.assertNotContains(response, "Yellowstone")
        self.assertNotContains(response, "Yosemite")
        self.assertNotContains(response, "Glacier National Park")

        #favorite yosemite
        add = 1
        park = Parks.objects.get(name='Yosemite').id
        fields = {'park': park, 'add': add}
        response = self.client.post(reverse("favorite_park", kwargs={'add':add, 'parkid':park}), fields)
        #should redirect back to the parks page
        self.assertEqual(response.status_code, 302)

        #Check if yosemite is a favorite
        response = self.client.get(reverse('parks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yosemite")
        self.assertNotContains(response, "Glacier National Park")
        self.assertNotContains(response, "Yellowstone")

        # unfavorite yosemite
        add = 0
        park = Parks.objects.get(name='Yosemite').id
        fields = {'park': park, 'add': add}
        response = self.client.post(reverse("favorite_park", kwargs={'add':add, 'parkid':park}), fields)
        # should redirect back to the parks page
        self.assertEqual(response.status_code, 302)

        #Ensure that the park was removed as a favorite
        response = self.client.get(reverse('parks'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Yellowstone")
        self.assertNotContains(response, "Yosemite")
        self.assertNotContains(response, "Glacier National Park")
