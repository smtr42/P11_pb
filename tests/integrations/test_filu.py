from django.shortcuts import reverse
from django.test import TestCase

from products.managers import ProductManager
from products.models import Category, Favorite, Product
from users.models import User


class FiluTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(FiluTest, cls).setUpClass()
        cls.test_user1 = User.objects.create_user(
            username="testuser1", email="test@test.com", password="1X<ISRUkw+tuK",
        )

    def test_route_user(self):
        self.client.force_login(user=self.test_user1)
        response = self.client.post(reverse("filu:uploadpage"))
        self.assertEqual(response.status_code, 200)

    def test_valid_doc(self):
        self.client.force_login(user=self.test_user1)
        f = open("tests/file/dummy.csv", "r")
        response = self.client.post(reverse("filu:filu"), {"file":f})
        self.assertEqual()

