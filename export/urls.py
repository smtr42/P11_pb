from django.urls import include, path

from .views import export

app_name = "export"
urlpatterns = [
    path("", export, name="export"),
]
