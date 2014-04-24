from django.conf.urls import patterns, url
from MWG_Site import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^login-error/', views.LoginError.as_view(), name='login-error'),
    url(r'^dashboard/', views.Dashboard.as_view(), name='dashboard'),
    url(r'^event/', views.EventDetails.as_view(), name='event-details'),
)

