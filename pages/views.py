from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    # https://docs.djangoproject.com/fr/2.2/topics/class-based-views/#subclassing-generic-views
    template_name = "pages/index.html"


class NoticePageView(TemplateView):
    template_name = "pages/notice.html"


@login_required(login_url="/accounts/login/")
class MyFood(TemplateView):
    template_name = "pages/myfood.html"


@login_required(login_url="/accounts/login/")
def Profile(request):
    user = request.user
    return render(request, "pages/account.html", {"user": user})
