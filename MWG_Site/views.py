from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


def home(request):
    if request.user and request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    return render(request, 'landing.html')


class Login(TemplateView):
    template_name = "landing.html"

@login_required
def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('landing.html')


class LoginError(TemplateView):
    template_name = "login_error.html"


class EventDetails(TemplateView):
    template_name = "event.html"


class Dashboard(TemplateView):
    template_name = "dashboard.html"


@login_required
def profile(request):
    user = request.user

