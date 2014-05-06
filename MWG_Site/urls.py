from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from MyWolfpackGuide import settings
from MWG_Site import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^scrape/', views.Scrape.as_view(), name='scrape'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^login-error/', views.LoginError.as_view(), name='login-error'),
    url(r'^events/browse/$', login_required(views.BrowseEvents.as_view()), name='browse-events'),
    url(r'^events/me/$', login_required(views.MyEvents.as_view()), name='my-events'),
    url(r'^events/create/$', login_required(views.CreateEvent.as_view()), name='create-event'),
    url(r'^events/edit/(?P<pk>\w+)', login_required(views.UpdateEvent.as_view()), name='update-event'),
    url(r'^events/remove/(?P<pk>\w+)', login_required(views.RemoveEvent.as_view()), name='remove-event'),
    url(r'^events/attend/(?P<pk>\w+)', login_required(views.AttendEvent.as_view()), name='attend-event'),
    url(r'^events/unattend/(?P<pk>\w+)', login_required(views.UnAttendEvent.as_view()), name='unattend-event'),
    url(r'^events/details/(?P<pk>\w+)', login_required(views.EventDetails.as_view()), name='event-details'),

)

##### do not do this in production
if settings.DEBUG:
	urlpatterns += patterns('',
	        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
	        'document_root': settings.MEDIA_ROOT}))

