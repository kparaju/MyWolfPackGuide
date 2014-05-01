from django.conf.urls import patterns, url
from MWG_Site import views
from MyWolfpackGuide import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^login-error/', views.LoginError.as_view(), name='login-error'),
    url(r'^events/browse/$', views.BrowseEvents.as_view(), name='browse-events'),
    url(r'^events/my/$', views.MyEvents.as_view(), name='my-events'),
    url(r'^events/create/', views.create_event, name='create-event'),
    url(r'^events/details/(?P<pk>\w+)', views.EventDetails.as_view(), name='event-details'),
)

##### do not do this in production
if settings.DEBUG:
	urlpatterns += patterns('',
	        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
	        'document_root': settings.MEDIA_ROOT}))

