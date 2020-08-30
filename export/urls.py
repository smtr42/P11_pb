from django.urls import path

from .views import export

app_name = "export"
urlpatterns = [
    path("", export, name="export"),
]
