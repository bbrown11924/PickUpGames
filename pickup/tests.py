from .models import Profile
from pickup.account_tests import *
from pickup.park_tests import *


# Test cases to make sure that pages exist
class PageExistenceTests(TestCase):

    def test_admin_page_exists(self):
        """
        Makes sure the admin page can be accessed
        """
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)


class IndexPageTests(TestCase):
    def test_index_page_exists(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class DatabaseTests(TestCase):

    def test_height_string_functionality(self):
        # Insert an element into the profile database
        q = Profile(name="Benjamin", weight = 160, height = 67)
        q.save()
        #Check if the proper height string is returned
        self.assertIs('5\'7\"' == q.get_height_cust(), True)