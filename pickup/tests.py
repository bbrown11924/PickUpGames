from django.test import TestCase


# Test cases to make sure that pages exist
class PageExistenceTests(TestCase):

    def test_admin_page_exists(self):
        """
        Makes sure the admin page can be accessed
        """
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)