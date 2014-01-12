from django.conf.urls import patterns, include, url
from glide.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jp.views.home', name='home'),
    # url(r'^jp/', include('jp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^profile/(\d{1,2})/$', profile),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                    'document_root': settings.MEDIA_ROOT}))
