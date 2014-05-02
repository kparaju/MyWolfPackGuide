from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from MWG_Site import views
from MyWolfpackGuide import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^login-error/', views.LoginError.as_view(), name='login-error'),
    url(r'^events/browse/$', login_required(views.BrowseEvents.as_view()), name='browse-events'),
    url(r'^events/me/$', login_required(views.MyEvents.as_view()), name='my-events'),
    url(r'^events/create/', login_required(views.CreateEvent.as_view()), name='create-event'),
    url(r'^events/create/submit$', require_POST(views.EventFormView.as_view()), name='event-form-submit'),
    url(r'^events/details/(?P<pk>\w+)', login_required(views.EventDetails.as_view()), name='event-details'),
)

##### do not do this in production
if settings.DEBUG:
	urlpatterns += patterns('',
	        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
	        'document_root': settings.MEDIA_ROOT}))

