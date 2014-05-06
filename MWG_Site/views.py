from django.views.generic import TemplateView, DetailView, View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import UpdateView
from MWG_Site.custom_views import MultipleFormsMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from MWG_Site.forms import EventForm, AddressForm, TagForm
import datetime
from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import AuthFailed, AuthCanceled
from MWG_Site.models import Event, Address, MWGUser, Tag
from tasks import scrape

def home(request):
    if request.user and request.user.is_authenticated():
        return redirect(reverse('browse-events'))
    return render(request, 'landing.html')

class AttendEvent(TemplateView):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        mwguser = MWGUser.objects.get(user=user)
        event = Event.objects.get(pk=kwargs['pk'])
        event.attendees.add(mwguser)
        return HttpResponseRedirect(reverse('event-details', kwargs={'pk': kwargs['pk']}))


class Scrape(TemplateView):
    def get(self, request, *args, **kwargs):
        scrape()
        return HttpResponseRedirect(reverse('browse-events'))


class UnAttendEvent(TemplateView):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        mwguser = MWGUser.objects.get(user=user)
        event = Event.objects.get(pk=kwargs['pk'])
        event.attendees.remove(mwguser)
        return HttpResponseRedirect(reverse('event-details', kwargs={'pk': kwargs['pk']}))


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
            events = user.attending.filter(time__range=(day, day+datetime.timedelta(days=1)))
            week.append({day:events})

        context['week'] = week
        context['mwguser'] = MWGUser.objects.get(user=self.request.user)
        return context


class Dashboard(BaseView, View):

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        user = MWGUser.objects.get(user=self.request.user)
        context['mwguser'] = user
        my_events = user.my_events | user.attending.all()
        context['my_events'] = my_events.distinct()
        context['dash_events']  = Event.objects.filter(time__gte=datetime.datetime.now())
        context['page'] = 'create'
        context['tags'] = Tag.objects.all()
        return context


class CreateEvent(Dashboard, TemplateResponseMixin, MultipleFormsMixin):

    template_name = 'events/create.html'

    form_classes = {
        'event_form': EventForm,
        'address_form': AddressForm,
        'tag_form':TagForm,
    }

    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))
 
    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)

        if all([form.is_valid() for form in forms.values()]):

            # Get User Object
            mwg_user = MWGUser.objects.get(user=self.request.user)

            # Save the Address Form
            address_form = forms.get('address_form')

            address, created = Address.objects.get_or_create(
                line_1=address_form.cleaned_data['line_1'],
                line_2=address_form.cleaned_data['line_2'],
                city=address_form.cleaned_data['city'],
                state_abbrev=address_form.cleaned_data['state_abbrev'],
                zipcode=address_form.cleaned_data['zipcode'],
            )

            # Get or Create Tag for Event
            tag_form = forms.get('tag_form')
            if tag_form.cleaned_data['existing_tag']:
                tag = tag_form.cleaned_data['existing_tag']
            else:
                tag = tag_form.cleaned_data['new_tag']

            event_tag, create = Tag.objects.get_or_create(
                name    = tag
                )

            # Get the values from the Event Form
            event = forms.get('event_form').instance
            event.address = address
            event.created_by=mwg_user
            event.save()

            event.tags.add(event_tag)
            event.save()

            # Redirect to the Event Details Page
            return HttpResponseRedirect(reverse('event-details', kwargs={'pk':event.pk}))
        else:
            return self.forms_invalid(forms)


class UpdateEvent(Dashboard, UpdateView):
    model  = Event
    fields = ['name', 'picture', 'description', 'price', 'time', 'address', 'tags']
    template_name_suffix = "_edit"

class RemoveEvent(View):

    def get(self, request, *args, **kwargs):
        mwg_user = get_object_or_404(MWGUser, user=request.user)
        event = Event.objects.get(pk=kwargs['pk'])
        if event.created_by.pk == mwg_user.pk:
            event.delete()
            return HttpResponseRedirect(reverse('my-events'))
        else:
            return HttpResponseForbidden()

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
        events = user.my_events | user.attending.all()
        events = events.order_by("time").distinct()
        
        times = {}

        for event in events:
            foo = ' '.join([event.time.strftime("%B"), str(event.time.year)])
            if not foo in times:
                times[foo] = []
            times[foo].append(event)

        print times
        context['times'] = times

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

