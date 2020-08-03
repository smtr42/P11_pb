from django.urls import path

from .views import upload_file, Importfile

app_name = "filu"
urlpatterns = [
    path("", upload_file, name="filu"),
    path("importfile", Importfile.as_view(), name="importfile"),
]
