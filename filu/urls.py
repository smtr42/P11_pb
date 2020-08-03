from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import Uploadpage, upload_file

app_name = "filu"
urlpatterns = [
    path("", upload_file, name="filu"),
    path(
        "uploadpage", login_required(Uploadpage.as_view()), name="uploadpage"
    ),
]
