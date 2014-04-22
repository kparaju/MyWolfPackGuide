from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user and request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    return render(request, 'login.html')


class Login(TemplateView):
    template_name = "login.html"


class LoginError(TemplateView):
    template_name = "login_error.html"


class EventDetails(TemplateView):
    template_name = "event.html"


class Dashboard(TemplateView):
    template_name = "dashboard.html"


@login_required
def profile(request):
    user = request.user

