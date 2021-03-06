from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'userbase.views.home', name='home'),
	url(r'^register/(?P<code>\w{26})/$', 'userbase.views.reg', name='register'),
	url(r'^register/$', 'userbase.views.reg', name='register'),
	url(r'^confirm/(?P<code>\w{26})/$', 'userbase.views.confirm', name='confirm'),
	url(r'^success/$', 'userbase.views.success', name='success'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'login.html'}, name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	(r'^user/', include('userbase.urls')),
	(r'^messages/', include('private_messages.urls')),
	(r'^forums/', include('forums.urls')),
	(r'^api/', include('userbase.api.urls')),
	#(r'^blogs/', include('blogs.urls')),
	(r'^admin/', include(admin.site.urls)),
	
	# Example:
	# (r'^benzene/', include('benzene.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	 #(r'^admin/', include(admin.site.urls)),
)

# development only
from django.views.static import serve
urlpatterns += patterns('', (r'^static/(?P<path>.*)$', serve, {'document_root': 'static'}),)
