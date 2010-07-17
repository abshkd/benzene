from django.conf.urls.defaults import *

import userbase.views
import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('',
	('^$', userbase.views.home),
	('^register/$', userbase.views.reg),
	('^confirm/$', userbase.views.confirm),
	('^success/$', userbase.views.success),
	('^login/$', 'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
	('^profile/$', userbase.views.profile),
	('^profile/(?P<user_name>.*)/edit/$', userbase.views.edit_profile),
	('^profile/(?P<user_name>.*)/$', userbase.views.profile),
	('^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/'}),
	('^torrents/$', userbase.views.torrents_view),
	('^test/$', userbase.views.test),
	
	# Example:
	# (r'^benzene/', include('benzene.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	 #(r'^admin/', include(admin.site.urls)),
)
