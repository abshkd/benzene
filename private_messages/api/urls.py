#userbase api urls
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import OAuthAuthentication
from handlers import MessageHandler

auth = {'authentication': OAuthAuthentication(realm="Benzene Realm") }
message = Resource(handler=MessageHandler, **auth)

urlpatterns = patterns('',
	url(r'^view/$', message),
	url(r'^view/(?P<id>\d*)/$', message),
	url(r'^send/$', message),
)
