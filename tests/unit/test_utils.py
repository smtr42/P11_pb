from unittest.mock import patch

from django.test import TestCase

from openfoodfact.utils import Cleaner, RequestData


class UtilsTest(TestCase):
    def test_product_request(self):
        def fetch_cat_mock():
            return ["sabji"]

        request_data = RequestData()

        with patch.object(request_data, "_fetch_category", fetch_cat_mock):
            self.assertIsInstance(request_data.exec(20), dict)
            self.assertEqual(
                request_data.exec(20)["sabji"]["products"][0][
                    "product_name_fr"
                ],
                "Indisches Sabji",
            )
            self.assertEqual(
                request_data.exec(20),
                {
                    "sabji": {
                        "products": [
                            {
                                "product_name_fr": "Indisches Sabji",
                                "id": "4260155025099",
                                "image_ingredients_url": "https://static."
                                "openfoodfacts.org/images/products/426/015/502"
                                "/5099/ingredients_fr.10.400.jpg",
                                "image_front_url": "https://static."
                                "openfoodfacts.org/images/products/426/015/502"
                                "/5099/front_fr.7.400.jpg",
                                "nutrition_grade_fr": "c",
                                "url": "https://fr.openfoodfacts.org/produit/"
                                "4260155025099/indisches-sabji-jooti",
                            }
                        ],
                        "skip": 0,
                        "page": "1",
                        "page_size": "20",
                        "count": 1,
                    }
                },
            )

    def test_category_request(self):
        def fetch_products_mock(*args, **kwargs):
            return {
                "sabji": {
                    "products": [
                        {
                            "product_name_fr": "Indisches Sabji",
                            "id": "4260155025099",
                            "image_ingredients_url": "https://static."
                            "openfoodfacts.org/images/products/426/015/502"
                            "/5099/ingredients_fr.10.400.jpg",
                            "image_front_url": "https://static.openfoodfacts."
                            "org/images/products/426/015/502/5099/front_fr."
                            "7.400.jpg",
                            "nutrition_grade_fr": "c",
                            "url": "https://fr.openfoodfacts.org/produit/"
                            "4260155025099/indisches-sabji-jooti",
                        }
                    ],
                    "skip": 0,
                    "page": "1",
                    "page_size": "20",
                    "count": 1,
                }
            }

        request_data = RequestData()

        with patch.object(
            request_data, "_fetch_products", fetch_products_mock
        ):
            self.assertIsInstance(request_data.exec(20), dict)
            self.assertEqual(
                request_data.list_cat,
                [
                    "Aliments et boissons à base de végétaux",
                    "Aliments d'origine végétale",
                    "Snacks",
                    "Snacks sucrés",
                    "Boissons",
                    "Produits laitiers",
                    "Viandes",
                    "Aliments à base de fruits et de légumes",
                    "Plats préparés",
                    "Céréales et pommes de terre",
                    "Produits fermentés",
                    "Produits laitiers fermentés",
                    "Produits à tartiner",
                    "Biscuits et gâteaux",
                    "Charcuteries",
                    "Epicerie",
                    "Petit-déjeuners",
                ],
            )


class TestCleaner(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data_good = {
            "id": "5410188031072",
            "product_name_fr": "Gazpacho",
            "nutrition_grade_fr": "a",
            "url": "https://fr.openfoodfacts.org/produit/5410188031072/"
            "gazpacho-alvalle",
            "image_front_url": "https://static.openfoodfacts.org/images/"
            "products/541/018/803/1072/front_fr.30.400.jpg",
            "image_ingredients_url": "https://static.openfoodfacts.org/images"
            "/products/541/018/803/1072/ingredients_fr.80.400.jpg",
        }
        cls.data_miss = {
            "id": "3228857000166",
            "product_name_fr": "Pain 100% mie complet",
            "url": "https://fr.openfoodfacts.org/produit/3228857000166/"
            "pain-100-mie-complet-harrys",
            "image_front_url": "https://static.openfoodfacts.org/images/"
            "products/322/885/700/0166/front_fr.97.400.jpg",
            "image_ingredients_url": "https://static.openfoodfacts.org/images"
            "/products/322/885/700/0166/ingredients_fr.51.400.jpg",
        }
        cls.data_empty = {
            "id": "",
            "product_name_fr": "Pain 100% mie complet",
            "url": "https://fr.openfoodfacts.org/produit/3228857000166/"
            "pain-100-mie-complet-harrys",
            "image_front_url": "https://static.openfoodfacts.org/images/"
            "products/322/885/700/0166/front_fr.97.400.jpg",
            "image_ingredients_url": "https://static.openfoodfacts.org/"
            "images/products/322/885/700/0166/ingredients_fr.51.400.jpg",
        }
        cls.data_bad_id = {
            "id": "31552503587",
            "product_name_fr": "Primevère Bio Tartine & Cuisson",
            "nutrition_grade_fr": "c",
            "url": "https://fr.openfoodfacts.org/produit/3155250358788/"
            "primevere-bio-tartine-cuisson",
            "image_front_url": "https://static.openfoodfacts.org/images/"
            "products/315/525/035/8788/front_fr.89.400.jpg",
            "image_ingredients_url": "https://static.openfoodfacts.org/"
            "images/products/315/525/035/8788/ingredients_fr.122.400.jpg",
        }

        args = {}
        cls.cleaner = Cleaner(args)

    def test_data_missing_key(self):
        existance = self.cleaner._data_exist(self.data_miss)
        self.assertEqual(existance, False)

    def test_data_empty_value(self):

        existance = self.cleaner._data_exist(self.data_empty)
        self.assertEqual(existance, False)

    def test_data_bad_id(self):
        existance = self.cleaner._data_exist(self.data_bad_id)
        self.assertEqual(existance, False)

    def test_double_barcode(self):
        self.cleaner.barcode_list.append(int(self.data_good["id"]))
        existance = self.cleaner._data_exist(self.data_good)
        self.assertEqual(existance, False)

    def test_barcode_not_in_barcodelist(self):
        self.cleaner._data_exist(self.data_good)
        self.assertIn(
            int(self.data_good["id"]), self.cleaner.barcode_list,
        )

    def test_double_name(self):
        self.cleaner.name_list.append(
            self.data_good["product_name_fr"].lower()
        )
        existance = self.cleaner._data_exist(self.data_good)
        self.assertEqual(existance, False)

    def test_name_not_in_namelist(self):
        self.cleaner._data_exist(self.data_good)
        self.assertIn(
            self.data_good["product_name_fr"].lower(), self.cleaner.name_list,
        )
