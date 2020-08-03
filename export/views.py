from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

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

    # qs_favs == <QuerySet [{'product_id': 1399, 'substitute_id': 1324}, {'product_id': 2817, 'substitute_id': 2881}]>
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
    # csv_data == [{'barcode': '3270160202706', 'product_name': 'Aiguillettes de poulet saveur citron surgelées'},
    #               {'barcode': '3564700038062', 'product_name': 'Jambon cru recette italienne'},
    #               {'barcode': '3292070006571', 'product_name': 'Houmous extra citron confit'},
    #               {'barcode': '3017620422003', 'product_name': 'Nutella'}]

    csv_data = [list(element.values()) for element in csv_data]
    # csv_data == [['3270160202706', 'Aiguillettes de poulet saveur citron surgelées'],
    #               ['3564700038062', 'Jambon cru recette italienne'],
    #               ['3292070006571', 'Houmous extra citron confit'],
    #               ['3017620422003', 'Nutella']]

    for i in range(len(csv_data)):
        if (i % 2) == 0:
            for element in csv_data[i + 1]:
                csv_data[i].append(element)
            else:
                pass
    del csv_data[1::2]

    csv_data.insert(0, ["barcode", "product_name"])

    template = loader.get_template("csv.txt")
    context = {"data": csv_data}
    response.write(template.render(context))
    return response
