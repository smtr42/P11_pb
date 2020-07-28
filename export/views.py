from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from products.managers import ProductManager
from products.models import Products


# Create your views here.
def export(request):
    """Export favorites into a file."""
    ProductManager.get_fav()

    response = HttpResponse(content_type="text/csv")
    fields = [
        "id",
        "product",
        "substitute",
    ]
    csv_data = ProductManager.get_fav() #return a list
    csv_data.insert(0, [field.verbose_name for field in Products._meta.fields])
    template = loader.get_template("export/csv.txt")
    context = {"data": csv_data}
    response.write(template.render(context))

    return response
