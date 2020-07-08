from django.conf import settings
from django.db import models

from . import managers


class Category(models.Model):
    """Handle the categories information."""

    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    """Handle the Product information."""

    objects = managers.ProductManager()

    barcode = models.CharField(max_length=13, unique=True)
    product_name = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=1)
    url = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    image_nut_url = models.CharField(max_length=255)
    categories = models.ManyToManyField("Category", related_name="products")

    def __str__(self):
        return self.product_name


class Favorite(models.Model):
    """This will regroup the product and its substitute associated with a
    user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="favorites",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        "Product",
        related_name="favorites_as_product",
        on_delete=models.CASCADE,
    )
    substitute = models.ForeignKey(
        "Product", related_name="fav_substitute", on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} subs {self.product} for {self.substitute}"
