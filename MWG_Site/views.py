from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from django.shortcuts import redirect
from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import AuthFailed

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


class MWGSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        if isinstance(exception, AuthFailed):
           return 'login-error'
        else:
            return super(MWGSocialAuthExceptionMiddleware, self)\
                                 .get_redirect_uri(request, exception)


@login_required
def profile(request):
    user = request.user

