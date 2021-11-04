# File: maps_test.py
# Author: Mansoor SHehzad
#
# This file contains tests for  opening the maps page.

from .models import Profile
from django.test import TestCase
from django.urls import reverse

# Test cases to make sure that pages exist
class PageExistenceTests(TestCase):

    def test_admin_page_exists(self):
        """
        Makes sure the maps page can be accessed
        """
        response = self.client.get(reverse("maps"))
        self.assertEqual(response.status_code, 302)

