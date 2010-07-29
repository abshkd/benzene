#notifications urls
from django.conf.urls.defaults import *
from notifications import views

urlpatterns = patterns('',
	url(r'^handle/$', views.delete_redirect, name='handle_notification'),
)