from django.test import TestCase
from rest_framework.test import APITestCase


class UserTest(APITestCase):
    def test_func1(self):
        self.assertEqual(1, 1)
