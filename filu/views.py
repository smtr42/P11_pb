from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.generic import FormView

from products.models import Product

from .forms import UploadFileForm


class Uploadpage(FormView):
    template_name = "filu/upload.html"
    form_class = UploadFileForm


@login_required(login_url="/accounts/login/")
def upload_file(request):
    if request.method == "POST" and request.FILES["file"]:
        myfile = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        Product.objects.read_and_import(request, myfile.name)

        return render(
            request,
            "pages/myfood.html",
            {"uploaded_file_url": uploaded_file_url},
        )
    return render(request, "pages/myfood.html")
