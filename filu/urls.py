from django.urls import path

from .views import upload_file

app_name = "filu"
urlpatterns = [
    path("", upload_file, name="filu"),
]
