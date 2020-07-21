from django.shortcuts import render
from products.managers import ProductManager

# Create your views here.
def export(request):
    """Export favorites into a file."""
    ProductManager.get_fav()
    
    pass
