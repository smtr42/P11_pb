from django.shortcuts import reverse
from django.test import TestCase

from products.managers import ProductManager
from products.models import Category, Favorite, Product
from users.models import User
import os

class FiluTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(FiluTest, cls).setUpClass()
        cls.test_user1 = User.objects.create_user(
            username="testuser1",
            email="test@test.com",
            password="1X<ISRUkw+tuK",
        )
        cls.test_category = Category.objects.create(category_name="Viandes")
        cls.test_product = Product.objects.create(
            barcode="3449865294044",
            product_name="Rosette",
            nutriscore="e",
            url="https://fr.openfoodfacts.org/produit/3449865294044/"
            "rosette-cochonou",
            image_url="https://static.openfoodfacts.org/images/products/"
            "344/986/529/4044/front_fr.28.400.jpg",
            image_nut_url="https://static.openfoodfacts.org/images/products/"
            "344/986/529/4044/ingredients_fr.12.400.jpg",
        )
        cls.test_product.categories.add(cls.test_category)

        cls.test_product2 = Product.objects.create(
            barcode="9999999999999",
            product_name="NESQUIK Moins de Sucres Poudre Cacaotée boîte",
            nutriscore="a",
            url="https://test",
            image_url="https://test",
            image_nut_url="https://test",
        )

    def test_route_user(self):
        self.client.force_login(user=self.test_user1)
        response = self.client.post(reverse("filu:uploadpage"))
        self.assertEqual(response.status_code, 200)

    def test_valid_doc(self):
        self.client.force_login(user=self.test_user1)
        dummy_file_str_path = "tests/file/dummy.csv"
        media_str_path = "media/dummy.csv"
        f = open(dummy_file_str_path, "r")
        response = self.client.post(reverse("filu:filu"), {"file": f})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorite.objects.count(), 1)
        self.assertFalse(os.path.isfile(media_str_path))
