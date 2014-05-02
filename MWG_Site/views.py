from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
from MWG_Site.forms import EventForm, AddressForm
import datetime
# from django.contrib.auth.decorators import login_required
from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import AuthFailed, AuthCanceled
from MWG_Site.models import Event, Address, MWGUser

def home(request):
    if request.user and request.user.is_authenticated():
        return redirect(reverse('browse-events'))
    return render(request, 'landing.html')


class Login(TemplateView):
    template_name = "landing.html"


class LoginError(TemplateView):
    template_name = "login_error.html"


class BaseView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        today = datetime.date.today()
        week  = []
        for day in range(0,7):
            week.append(today + datetime.timedelta(days=day))

        context['week'] = week
        return context


class Dashboard(BaseView, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        user = self.request.user
        context['mwguser'] = MWGUser.objects.get(user=user)
        context['events']  = Event.objects.all()
        return context


# @login_required
# def create_event(request):
#     if request.method == 'POST':
#         event_form = EventForm(request.POST)
#         address_form = AddressForm(request.POST)
#         if event_form.is_valid() and address_form.is_valid():
#             #cleaned_data = form.cleaned_data
#             event = Event(**event_form.cleaned_event_data)
#             address = Address(**address_form.cleaned_address_data)
#             address.save()
#             event.address = address
#             event.save()
#             return HttpResponseRedirect(reverse('event_details', args=[event.pk]))
#     else:
#         event_form = EventForm()
#         print event_form

#         address_form = AddressForm()

#     return render(request, 'events/create.html', {
#         'event_form': event_form,
#         'address_form': address_form,
#     })


class CreateEvent(Dashboard, TemplateView):
    template_name = 'events/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateEvent, self).get_context_data(**kwargs)
        context['event_form'] = EventForm
        context['address_form'] = AddressForm
        return context


class EventFormView(FormView):
    form_class = EventForm
    success_url = '/'


class AddressFormView(FormView):
    form_class = AddressForm
    success_url = '/'


class BrowseEvents(Dashboard, TemplateView):
    template_name = "events/browse.html"

    def get_context_data(self, **kwargs):
        context = super(BrowseEvents, self).get_context_data(**kwargs)
        context['events']  = Event.objects.all()
        return context


class MyEvents(Dashboard, TemplateView):
    template_name = "events/myevents.html"

    def get_context_data(self, **kwargs):
        context = super(MyEvents, self).get_context_data(**kwargs)

        user = self.request.user
        context['events'] = Event.objects.filter(created_by=user)
        return context


class EventDetails(DetailView, BaseView):
    model = Event
    pk_url_kwarg = 'pk'
    context_object_name = 'event'
    template_name = "events/details.html"


class MWGSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        if isinstance(exception, AuthFailed) or isinstance(exception, AuthCanceled):
           return 'login-error'
        else:
            return super(MWGSocialAuthExceptionMiddleware, self)\
                                 .get_redirect_uri(request, exception)

