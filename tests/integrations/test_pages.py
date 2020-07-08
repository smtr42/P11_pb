from django.test import TestCase
from django.urls import reverse

from products.models import Category, Favorite, Product
from users.models import User


class LoggedInTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(LoggedInTest, cls).setUpClass()
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

    def testLogin(self):

        self.client.login(email="test@test.com", password="1X<ISRUkw+tuK")

        response = self.client.get(reverse("pages:profile"))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email="test@test.com", password="1X<ISRUkw+tuK")

        response = self.client.get(reverse("pages:profile"))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email="test@test.com", password="1X<ISRUkw+tuK")

        response = self.client.get(reverse("pages:profile"))
        self.assertEqual(response.status_code, 200)

    def test_user_exists(self):
        user = User.objects.get(username="testuser1")
        self.assertEqual(user.username, "testuser1")

    def test_can_save_product(self):
        product = {
            "product-searched-name": ["Rosette"],
            "product-searched-id": ["1"],
            "product-searched-barcode": ["3449865294044"],
            "product-searched-nutriscore": ["e"],
            "substitute-searched-name": [
                "NESQUIK Moins de Sucres Poudre Cacaotée boîte"
            ],
            "substitute-searched-id": ["2"],
            "substitute-searched-barcode": [""],
            "substitute-searched-nutriscore": ["a"],
        }
        self.client.force_login(user=self.test_user1)
        response = self.client.post(reverse("products:save"), data=product)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorite.objects.count(), 1)

    def test_can_view_favorite(self):
        self.client.login(email="test@test.com", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("products:fav"))
        self.assertEqual(response.status_code, 200)

    def test_autocomplete_view(self):
        data = {"term": "Rose"}
        response = self.client.get(reverse("autocomplete:complete"), data)
        self.assertEqual(response.status_code, 200)
        products = Product.objects.get_all_by_term(data["term"])
        products = [product.product_name for product in products]

        self.assertEqual(products, ["Rosette"])
