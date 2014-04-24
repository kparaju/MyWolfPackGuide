from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Django Admin Pages
    url(r'^admin/', include(admin.site.urls)),
    # MWG_Site App URLs
    url(r'^', include('MWG_Site.urls')),
    # Google Auth Login/Logout
    url(r'^auth/', include('social_auth.urls')),
)
 
