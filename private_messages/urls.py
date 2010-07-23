from django.conf.urls.defaults import *
from private_messages import views

urlpatterns = patterns('',
	(r'^$', views.summary),
	(r'^inbox/$', views.inbox), 
	