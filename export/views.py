from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.apps import apps

from products.managers import ProductManager
from products.models import Product


# Create your views here.
def export(request):
    """Export favorites into a file."""
    response = HttpResponse(content_type="text/csv")

    product_model = apps.get_model("products", "Product")
    favorite_model = apps.get_model("products", "Favorite")
    qs_favs = (
        favorite_model.objects.all()
        .filter(user=request.user)
        .values("product_id", "substitute_id")
    )
    favorite_qs_list = []

    for element in qs_favs:
        favorite_qs_list.append(
            product_model.objects.filter(id=element["substitute_id"]).values(
                "barcode", "product_name"
            )
        )
        favorite_qs_list.append(
            product_model.objects.filter(id=element["product_id"]).values(
                "barcode", "product_name"
            )
        )

    csv_data = [element[0] for element in favorite_qs_list]
    csv_data = [list(element.values()) for element in csv_data]
    csv_data.insert(0, ["barcode", "product_name"])
    template = loader.get_template("csv.txt")
    context = {"data": csv_data}
    response.write(template.render(context))
    return response
