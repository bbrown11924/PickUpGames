from django.test import TestCase

class navbar_tests(TestCase):
	def bar_exists_test(self):
		        response = self.client.get('/home/')
        		self.assertEqual(response.status_code, 200)
