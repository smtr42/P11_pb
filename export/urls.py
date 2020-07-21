from django.urls import include, path
from .views import export


urlpatterns = [
    path('export/', export ,name="export"),
]