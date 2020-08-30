from django.shortcuts import reverse
from django.test import TestCase

from products.managers import ProductManager
from products.models import Product


class Databasetest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(Databasetest, cls).setUpClass()
        cls.data = {
            "sabji": [
                {
                    "product_name_fr": "Indisches Sabji",
                    "id": "4260155025099",
                    "image_ingredients_url": "https://static.openfoodfacts."
                    "org/images/products/426/015/502/5099/ingredients_fr.10"
                    ".400.jpg",
                    "image_front_url": "https://static.openfoodfacts.org/"
                    "images/products/426/015/502/5099/front_fr.7.400.jpg",
                    "nutrition_grade_fr": "c",
                    "url": "https://fr.openfoodfacts.org/produit/"
                    "4260155025099/indisches-sabji-jooti",
                }
            ],
        }
        Product.objects.create_db_from_openfoodfacts(cls.data)

    def test_database_creation(self):
        product = Product.objects.filter(barcode=4260155025099).values(
            "product_name"
        )
        self.assertEqual(
            product[0]["product_name"],
            self.data["sabji"][0]["product_name_fr"],
        )

    def test_delete_database(self):
        product = product = Product.objects.all()
        self.assertEqual(len(product), 1)
        Product.objects.delete_data_in_tables()
        product = Product.objects.all()
        self.assertEqual(len(product), 0)


class SearchTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(SearchTest, cls).setUpClass()
        cls.data = {
            "sabji": [
                {
                    "product_name_fr": "Indisches Sabji",
                    "id": "4260155025099",
                    "image_ingredients_url": "https://static.openfoodfacts."
                    "org/images/products/426/015/502/5099/ingredients_fr"
                    ".10.400.jpg",
                    "image_front_url": "https://static.openfoodfacts.org/"
                    "images/products/426/015/502/5099/front_fr.7.400.jpg",
                    "nutrition_grade_fr": "c",
                    "url": "https://fr.openfoodfacts.org/produit/"
                    "4260155025099/indisches-sabji-jooti",
                },
                {
                    "id": "5410188031072",
                    "product_name_fr": "Gazpacho",
                    "nutrition_grade_fr": "a",
                    "url": "https://fr.openfoodfacts.org/produit/"
                    "5410188031072/gazpacho-alvalle",
                    "image_front_url": "https://static.openfoodfacts.org/"
                    "images/products/541/018/803/1072/front_fr.30.400.jpg",
                    "image_ingredients_url": "https://static."
                    "openfoodfacts.org/images/products/541/018/803/"
                    "1072/ingredients_fr.80.400.jpg",
                },
            ],
        }
        Product.objects.create_db_from_openfoodfacts(cls.data)

    def test_search_from_user_input(self):
        data = {"product": "Indisches Sabji"}
        (
            substitute,
            selected_product,
        ) = ProductManager.search_from_user_input(data)
        self.assertEqual(
            substitute[0]["product_name"],
            self.data["sabji"][1]["product_name_fr"],
        )
        self.assertEqual(
            selected_product[0]["product_name"],
            self.data["sabji"][0]["product_name_fr"],
        )

    def test_get_detail(self):

        data = {
            "product-image.x": ["161"],
            "product-image.y": ["263"],
            "product-id": 1,
        }
        response = self.client.post(reverse("products:detail"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/detail.html")

        qs_product = Product.objects.filter(id=data["product-id"]).values(
            "product_name",
            "nutriscore",
            "id",
            "url",
            "image_url",
            "image_nut_url",
            "barcode",
        )
        self.assertEqual(
            response.context[0]["product"][0]["product_name"],
            qs_product[0]["product_name"],
        )
        response = self.client.get(reverse("products:detail"), data=data)
        self.assertEqual(response.status_code, 404)
