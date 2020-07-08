from django.test import TestCase

from products.models import Category, Product
from users.models import User


class CategoryModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CategoryModelTest, cls).setUpClass()
        Category.objects.create(category_name="Sodas")

    def test_category_name_label(self):
        category = Category.objects.get(category_name="Sodas")
        field_label = category._meta.get_field("category_name").verbose_name
        self.assertEquals(field_label, "category name")

    def test_category_name_max_length(self):
        category = Category.objects.get(category_name="Sodas")
        max_length = category._meta.get_field("category_name").max_length
        self.assertEquals(max_length, 255)

    def test_object_name_is_model_name(self):
        category = Category.objects.get(category_name="Sodas")
        expected_object_name = category.category_name
        self.assertEquals(expected_object_name, str(category))


class ProductModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ProductModelTest, cls).setUpClass()
        Product.objects.create(
            barcode="1125896345237",
            product_name="Salade sans sauce",
            nutriscore="A",
            url="http://openfoodfact.fr/salade",
            image_url="http://openfoodfact.fr/img_salade",
            image_nut_url="http:/openfoodfact.fr/img_nut_url",
        )

    def test_product_barcode_label(self):
        product = Product.objects.get(barcode="1125896345237")
        field_label = product._meta.get_field("barcode").verbose_name
        self.assertEquals(field_label, "barcode")

    def test_product_barcode_max_length(self):
        product = Product.objects.get(barcode="1125896345237")
        max_length = product._meta.get_field("barcode").max_length
        self.assertEquals(max_length, 13)

    def test_product_name_label(self):
        product = Product.objects.get(barcode="1125896345237")
        field_label = product._meta.get_field("product_name").verbose_name
        self.assertEquals(field_label, "product name")

    def test_product_name_max_length(self):
        product = Product.objects.get(barcode="1125896345237")
        max_length = product._meta.get_field("product_name").max_length
        self.assertEquals(max_length, 255)

    def test_nutriscore_name(self):
        product = Product.objects.get(barcode="1125896345237")
        field_label = product._meta.get_field("nutriscore").verbose_name
        self.assertEquals(field_label, "nutriscore")

    def test_nutriscore_max_length(self):
        product = Product.objects.get(barcode="1125896345237")
        max_length = product._meta.get_field("nutriscore").max_length
        self.assertEquals(max_length, 1)

    def test_url_name(self):
        product = Product.objects.get(barcode="1125896345237")
        field_label = product._meta.get_field("url").verbose_name
        self.assertEquals(field_label, "url")

    def test_url_max_length(self):
        product = Product.objects.get(barcode="1125896345237")
        max_length = product._meta.get_field("url").max_length
        self.assertEquals(max_length, 255)

    def test_image_url_name(self):
        product = Product.objects.get(barcode="1125896345237")
        field_label = product._meta.get_field("image_url").verbose_name
        self.assertEquals(field_label, "image url")

    def test_image_url_max_length(self):
        product = Product.objects.get(barcode="1125896345237")
        max_length = product._meta.get_field("image_url").max_length
        self.assertEquals(max_length, 255)

    def test_image_nut_url_name(self):
        product = Product.objects.get(barcode="1125896345237")
        field_label = product._meta.get_field("image_nut_url").verbose_name
        self.assertEquals(field_label, "image nut url")

    def test_image_nut_url_max_length(self):
        product = Product.objects.get(barcode="1125896345237")
        max_length = product._meta.get_field("image_nut_url").max_length
        self.assertEquals(max_length, 255)

    def test_object_name_is_model_name(self):
        product = Product.objects.get(barcode="1125896345237")
        expected_object_name = product.product_name
        self.assertEquals(expected_object_name, str(product))


class UsersTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(UsersTest, cls).setUpClass()
        cls.test_user1 = User.objects.create_user(
            username="testuser1",
            email="test@test.com",
            password="1X<ISRUkw+tuK",
        )

    def test_user_name_is_email(self):
        user = User.objects.get(username="testuser1")
        self.assertEqual(str(user), user.email)
