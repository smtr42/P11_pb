from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.views.generic import TemplateView

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class Importfile(TemplateView):
    template_name = "filu/upload.html"


# def upload_file(request):
#     if request.method == "POST" and request.FILES["myfile"]:
#         myfile = request.FILES["myfile"]
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)

#         return render(
#             request,
#             "pages/myfood.html",
#             {"uploaded_file_url": uploaded_file_url},
#         )
#     return render(request, "pages/myfood.html")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            print("uploaded")
            return HttpResponseRedirect('pages:myfood')
    else:
        form = UploadFileForm()
    return render(request, 'pages/myfood.html', {'form': form})







def read_and_import():
    pass