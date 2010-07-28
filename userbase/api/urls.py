#userbase api urls
from django.conf.urls.defaults import *
from piston.resource import Resource
#from piston.authentication import OAuthAuthentication
from handlers import CustomUserHandler

#auth = {'authentication': OAuthAuthentication(realm="Benzene Realm") }

#customuser = Resource(handler=CustomUserHandler, **auth)
customuser = Resource(CustomUserHandler)

urlpatterns = patterns('',
	url(r'^user/(?P<post_slug>[^/]+)/', customuser)
)

urlpatterns += patterns('piston.authentication',
	url(r'^oauth/request_token/$', 'oauth_request_token'),
	url(r'^oauth/authorize/$', 'oauth_user_auth'),
	url(r'^oauth/access_token/$', 'oauth_access_token'),
)
