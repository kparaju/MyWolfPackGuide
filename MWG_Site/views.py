from django.views.generic import TemplateView, DetailView, View
from django.views.generic.base import TemplateResponseMixin
from MWG_Site.custom_views import MultipleFormsMixin
from django.core.urlresolvers import reverse
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
        context['dash_events']  = Event.objects.all()
        context['page'] = 'create'
        return context


class CreateEvent(Dashboard, TemplateResponseMixin, MultipleFormsMixin):

    template_name = 'events/create.html'

    form_classes = {
        'event_form': EventForm,
        'address_form': AddressForm,
    }

    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))
 
    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        
        print dir(forms.get('address_form').instance)

        if all([form.is_valid() for form in forms.values()]):


            # Get User Object
            user = self.request.user

            # Save the Address Form
            address_form = forms.get('address_form').instance

            address, created = Address.objects.get_or_create(
                line_1=address_form.line_1,
                line_2=address_form.line_2,
                city=address_form.city,
                state_abbrev=address_form.state_abbrev,
                zipcode=address_form.zipcode,
            )

            # Get the values from the Event Form
            event_form = forms.get('event_form').instance

            # Adapt time to timezone
            time = timezone.make_aware(event_form.time, timezone.get_current_timezone())

            #Save Event Object with user, address, and time
            event = Event.objects.create (
                name=event_form.name,
                description=event_form.description,
                price=event_form.price,
                picture = event_form.picture,
                time=time,
                address=address,
                created_by=user,
            )

            # Save the Event Object
            event.save()

            return HttpResponseRedirect(reverse('event-details', kwargs={'pk':event.pk}))
        else:
            return self.forms_invalid(forms)


class BrowseEvents(Dashboard, TemplateView):
    template_name = "events/browse.html"

    def get_context_data(self, **kwargs):
        context = super(BrowseEvents, self).get_context_data(**kwargs)
        context['events']  = Event.objects.filter(time__gte=datetime.datetime.now())
        context['page'] = 'browse'
        return context


class MyEvents(Dashboard, TemplateView):
    template_name = "events/myevents.html"

    def get_context_data(self, **kwargs):
        context = super(MyEvents, self).get_context_data(**kwargs)

        user = MWGUser.objects.get(user=self.request.user)
        context['events'] = user.events
        context['page'] = 'me'
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

