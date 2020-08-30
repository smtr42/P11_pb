from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from favoritecart.cart import FavoriteCart
from favoritecart.helpers import redirect_to_login
from products.forms import SearchForm
from products.managers import ProductManager


def sub_list(request):
    """Display the list of substitute for one selected product."""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            (
                substitute,
                selected_product,
            ) = ProductManager.search_from_user_input(form.cleaned_data)
            return render(
                request,
                "products/sub_list.html",
                {"product": substitute, "searched": selected_product},
            )
        else:
            print("form is not valid !")
            raise Http404
    else:
        form = SearchForm()
    return render(request, "products/sub_list.html", {"form": form})


def save(request):
    """Save the product into favorite."""
    if request.method == "POST":
        data = request.POST
        if not request.user.is_authenticated:
            cart = FavoriteCart(request)
            cart.add(
                {
                    "product": data["product-searched-id"],
                    "substitute": data["substitute-searched-id"],
                    "user": "user",
                }
            )
            return redirect_to_login(
                request, "/products/fav", login_url="/accounts/login/"
            )
        ProductManager.save_product(request, data)
        favs = ProductManager.get_fav(request)
        return render(request, "pages/myfood.html", {"favorites": favs})
    else:
        raise Http404


@login_required(login_url="/accounts/login/")
def fav(request):
    """Display favorites saved by user."""
    favs = ProductManager.get_fav(request)
    return render(request, "pages/myfood.html", {"favorites": favs})


def detail(request):
    """Display detail of a selected product."""
    if request.method == "POST":
        data = request.POST
        product_detail = ProductManager.get_detail(data)
        return render(
            request, "pages/detail.html", {"product": product_detail}
        )
    else:
        raise Http404
