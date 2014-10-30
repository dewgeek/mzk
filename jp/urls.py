from django.conf.urls import patterns, include, url
from db.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
from django.conf.urls.static import static
urlpatterns = patterns('',
    # Examples:
    url(r'^$', home),
    # url(r'^jp/', include('jp.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^meals/', meals),
    url(r'^breakfast/', meals),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^profile/(\d{1,2})/$', profile),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^orders/',receive_orders),
	url(r'^delete_order/',delete_order),
	url(r'^list_orders/',list_orders),
	url(r'^login/',login),
	url(r'^register/',register),
	url(r'^portal/',portal),
	url(r'^test/',test),
	url(r'^cart/',cart),
	url(r'^logout/',logout_view),
	url(r'^dashboard/',dashboard),
	url(r'^edit_order/',edit_order),
	url(r'^remove_order/',remove_db_order),
	url(r'^user/',end_user),
	url(r'^about/',about),
	url(r'^contact/',contact_us),
	url(r'^forgot_password/',forgot_password),
	url(r'^reset_pswd/',reset_pswd),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

