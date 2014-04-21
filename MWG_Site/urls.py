from django.conf.urls import patterns, url
from MWG_Site import views

urlpatterns = patterns('',
    url(r'^', views.Home.as_view(), name='home'),
)

