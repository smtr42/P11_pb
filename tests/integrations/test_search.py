from django.shortcuts import reverse
from django.test import TestCase

from products.models import Category, Product
from users.models import User


class Searchtest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(Searchtest, cls).setUpClass()
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
            barcode=3228857000166,
            product_name="Pain 100% mie complet",
            nutriscore="a",
            url="https://fr.openfoodfacts.org/produit/3228857000166/"
            "pain-100-mie-complet-harrys",
            image_url="https://static.openfoodfacts.org/images/products/"
            "322/885/700/0166/front_fr.97.400.jpg",
            image_nut_url="https://static.openfoodfacts.org/images/products/"
            "322/885/700/0166/ingredients_fr.51.400.jpg",
        )
        cls.test_product2.categories.add(cls.test_category)

        cls.test_product3 = Product.objects.create(
            barcode=5410188031072,
            product_name="Gazpacho",
            nutriscore="a",
            url="https://fr.openfoodfacts.org/produit/5410188031072/"
            "gazpacho-alvalle",
            image_url="https://static.openfoodfacts.org/images/products/"
            "541/018/803/1072/front_fr.30.400.jpg",
            image_nut_url="https://static.openfoodfacts.org/images/products/"
            "541/018/803/1072/ingredients_fr.80.400.jpg",
        )
        cls.test_product3.categories.add(cls.test_category)

    def test_substitute_from_search(self):
        data = {"product": "Rosette"}
        response = self.client.post(reverse("products:sub_list"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/sub_list.html")
