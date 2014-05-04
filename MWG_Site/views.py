from django.views.generic import TemplateView, DetailView, View
from MWG_Site.custom_views import MultipleFormsView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from MWG_Site.forms import EventForm, AddressForm
import datetime
from django.utils import timezone
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


class BaseView(View):

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        user = MWGUser.objects.get(user=self.request.user)
        today = datetime.date.today()
        week  = []
        for day in range(0,7):
            day = today + datetime.timedelta(days=day)
            events = user.events.filter(time__range=(day, day+datetime.timedelta(days=1)))
            week.append({day:events})

        context['week'] = week
        return context


class Dashboard(BaseView, View):

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        user = self.request.user
        context['mwguser'] = MWGUser.objects.get(user=user)
        context['events']  = Event.objects.all()
        return context


class CreateEvent(BaseView, MultipleFormsView):

    template_name = 'events/create.html'
    success_url = reverse_lazy('home')

    form_classes = {
        'event_form': EventForm,
        'address_form': AddressForm,
    }

    # def form_valid(self, form):

    #     # Get User Object
    #     user = self.request.user

    #     #Save Address Object
    #     address = Address.objects.get_or_create(
    #         line_1=form['line_1'],
    #         line_2=form['line_2'],
    #         city=form['city'],
    #         state_abbrev=form['state_abbrev'],
    #         zipcode=form['zipcode'],
    #     )

    #     # Adapt time to timezone
    #     time = timezone.make_aware(form['time'], timezone.get_current_timezone())

    #     #Save Event Object with user, address, and time
    #     event = Event.objects.create (
    #         name=form['name'],
    #         _picture=form['_picture'],
    #         description=form['description'],
    #         price=form['price'],
    #         time=time,
    #         address=address,
    #         created_by=user,
    #     )

    #     return HttpResponseRedirect(reverse(event.get_absolute_url))


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

        user = MWGUser.objects.get(user=self.request.user)
        context['events'] = user.events
        return context


class EventDetails(BaseView, DetailView):
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

