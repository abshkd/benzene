#userbase urls
from django.conf.urls.defaults import *
from userbase import views

urlpatterns = patterns('',
	url(r'^(?P<username>.*)/$', views.profile, name='profile'),
	url(r'^(?P<username>.*)/edit/$', views.edit_profile, name='edit_profile')
)