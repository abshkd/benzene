#userbase urls
from django.conf.urls.defaults import *
from userbase import views

urlpatterns = patterns('',
	url(r'^$', views.profile, name='default_profile'),
	url(r'^(?P<username>.*)/edit/$', views.edit_profile, name='edit_profile'),
	url(r'^(?P<username>.*)/$', views.profile, name='profile'),	
)
#as of now, edit_profile must come before profile, need better RE