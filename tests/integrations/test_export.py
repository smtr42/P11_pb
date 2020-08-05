from django.shortcuts import reverse
from django.test import TestCase

from products.managers import ProductManager
from products.models import Category, Favorite, Product
from users.models import User


class ExportTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ExportTest, cls).setUpClass()
        cls.test_user1 = User.objects.create_user(
            username="testuser1",
            email="test@test.com",
            password="1X<ISRUkw+tuK",
        )

        cls.test_category = Category.objects.create(category_name="Viandes")
        cls.test_product = Product.objects.create(
            barcode=3449865294044,
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
            barcode=9999999999999,
            product_name="NESQUIK Moins de Sucres Poudre Cacaotée boîte",
            nutriscore="a",
            url="https://test",
            image_url="https://test",
            image_nut_url="https://test",
        )

        cls.test_product3 = Product.objects.create(
            barcode=7777777777777,
            product_name="Ziguigoui",
            nutriscore="a",
            url="https://test",
            image_url="https://test",
            image_nut_url="https://test",
        )
        cls.test_favorite = Favorite.objects.create(
            user=cls.test_user1,
            product=cls.test_product,
            substitute=cls.test_product2,
        )

    def test_export_product(self):
        self.client.force_login(user=self.test_user1)
        response = self.client.post(reverse("export:export"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers["content-type"][1], "text/csv")
        self.assertEqual(response.templates[0].name, "csv.txt")
        self.assertEqual(
            response.context["data"][0], ["barcode", "product_name"]
        )
        self.assertEqual(
            response.context["data"][1][0], str(self.test_product2.barcode)
        )
        self.assertEqual(
            response.context["data"][1][2], str(self.test_product.barcode)
        )
