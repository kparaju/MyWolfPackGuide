from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user and request.user.is_authenticated():
        return redirect(reverse('browse-events'))
    return render(request, 'landing.html')


class Login(TemplateView):
    template_name = "landing.html"


class LoginError(TemplateView):
    template_name = "login_error.html"


class CreateEvent(TemplateView):
	template_name = "events/create.html"


class BrowseEvents(TemplateView):
	template_name = "events/browse.html"


class EventDetails(TemplateView):
    template_name = "events/details.html"



@login_required
def profile(request):
    user = request.user

