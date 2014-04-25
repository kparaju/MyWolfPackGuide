from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required


# from django.shortcuts import redirect
from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import AuthFailed

from MWG_Site import models

def home(request):
    if request.user and request.user.is_authenticated():
        return redirect(reverse('browse-events'))
    return render(request, 'landing.html')


class Login(TemplateView):
    template_name = "landing.html"


class LoginError(TemplateView):
    template_name = "login_error.html"

class Dashboard(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        user = self.request.user
        context['mwguser'] = models.MWGUser.objects.get(user=user)
        context['events']  = models.Event.objects.all()

        return context


class CreateEvent(Dashboard, TemplateView):
	template_name = "events/create.html"


class BrowseEvents(Dashboard, TemplateView):
	template_name = "events/browse.html"

class MyEvents(Dashboard, TemplateView):
	template_name = "events/myevents.html"


class EventDetails(TemplateView):
    template_name = "events/details.html"


class MWGSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        if isinstance(exception, AuthFailed):
           return 'login-error'
        else:
            return super(MWGSocialAuthExceptionMiddleware, self)\
                                 .get_redirect_uri(request, exception)

