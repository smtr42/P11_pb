from django.http import JsonResponse

from products.models import Product


def complete(request):
    """Get searched term and return a list of matching queries."""
    searched_term = request.GET.get("term")
    products = Product.objects.get_all_by_term(searched_term)
    products = [product.product_name for product in products]
    return JsonResponse(products, safe=False)
