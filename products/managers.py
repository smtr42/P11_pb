"""Database operations with a global scale."""
from django.apps import apps
from django.core.management.color import no_style
from django.db import IntegrityError, connection, models


class ProductManager(models.Manager):
    """Custom Object for Poroduct."""

    def create_db_from_openfoodfacts(self, data):
        """Save each product into the database."""
        product_model = apps.get_model("products", "Product")
        category_model = apps.get_model("products", "Category")
        print("Saving data into the database")
        for category in data:
            cat = category_model(category_name=category)
            cat.save()
            for p in data[category]:
                try:
                    prod = product_model(
                        barcode=p["id"],
                        product_name=p["product_name_fr"],
                        nutriscore=p["nutrition_grade_fr"],
                        url=p["url"],
                        image_url=p["image_front_url"],
                        image_nut_url=p["image_ingredients_url"],
                    )
                    prod.save()
                    prod.categories.add(cat)
                except IntegrityError:
                    pass

    def delete_data_in_tables(self):
        """Delete data in tables but not tables.

        To use before insertion.
        """
        product_model = apps.get_model("products", "Product")
        category_model = apps.get_model("products", "Category")
        favorite_model = apps.get_model("products", "Favorite")
        print("Deleting everything in database")

        category_model.objects.all().delete()
        product_model.objects.all().delete()
        favorite_model.objects.all().delete()
        sequence_sql = connection.ops.sequence_reset_sql(
            no_style(), [product_model, category_model, favorite_model]
        )
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

    @staticmethod
    def search_from_user_input(data):
        """Retrieve substitute from user search."""
        # https://docs.djangoproject.com/fr/3.0/ref/models/querysets/#field-lookups

        product_model = apps.get_model("products", "Product")
        name = data["product"]

        selected_product = product_model.objects.filter(
            product_name__iexact=name
        ).values()
        selected_product_category_name = product_model.objects.filter(
            product_name__iexact=name
        ).values("categories__category_name", "id")
        substitute = (
            product_model.objects.filter(
                categories__category_name=selected_product_category_name[0][
                    "categories__category_name"
                ],
                nutriscore__lt=selected_product[0]["nutriscore"],
            )
            .order_by("nutriscore")
            .values(
                "product_name",
                "nutriscore",
                "id",
                "url",
                "image_url",
                "image_nut_url",
            )[:6]
        )

        return substitute, selected_product

    @staticmethod
    def save_product(request, data):
        """Save the selected product into favorites."""
        favorite_model = apps.get_model("products", "Favorite")
        product_model = apps.get_model("products", "Product")

        product = product_model.objects.get(id=data["product-searched-id"])
        sub = product_model.objects.get(id=data["substitute-searched-id"])

        favorite_model.objects.create(
            user=request.user, product=product, substitute=sub
        )

    @staticmethod
    def get_fav(request):
        """Return the favorites of the user."""
        product_model = apps.get_model("products", "Product")
        favorite_model = apps.get_model("products", "Favorite")
        qs_favs = (
            favorite_model.objects.all()
            .filter(user=request.user)
            .values("product_id", "substitute_id")
        )
        favorite_list = []

        for element in qs_favs:
            favorite_list.append(
                product_model.objects.filter(
                    id=element["substitute_id"]
                ).values(
                    "product_name",
                    "nutriscore",
                    "id",
                    "url",
                    "image_url",
                    "image_nut_url",
                )
            )
        return favorite_list

    @staticmethod
    def get_detail(data):
        """Return details for a selected product."""
        product_model = apps.get_model("products", "Product")
        qs_product = product_model.objects.filter(
            id=data["product-id"]
        ).values(
            "product_name",
            "nutriscore",
            "id",
            "url",
            "image_url",
            "image_nut_url",
            "barcode",
        )
        return qs_product

    def get_all_by_term(self, term):
        """Filter product containing terms for autocomplete."""
        return self.filter(product_name__icontains=term)
