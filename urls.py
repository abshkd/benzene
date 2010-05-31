from django.conf.urls.defaults import *
import core.views

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('',
	('^$', core.views.home),
	('^registration/$', core.views.reg),
	('^confirm/(\w{14,26})', core.views.confirm),
	('^success/$', core.views.success),
	('^test/$', core.views.test),
    # Example:
    # (r'^benzene/', include('benzene.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #(r'^admin/', include(admin.site.urls)),
)
