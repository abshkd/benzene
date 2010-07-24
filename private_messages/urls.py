#private_messages urls
from django.conf.urls.defaults import *
from private_messages import views

urlpatterns = patterns('',
	url(r'^$', views.inbox, name='inbox'),
	url(r'^outbox/$', views.inbox, name='outbox', kwargs = {'outbox':True}),
	url(r'^view/(?P<key>\w{32})/$', views.view_conversation, name='view_conversation'),
	url(r'^send/(?P<recip>.*)/$', views.send_message, name='send_message'),
)
	