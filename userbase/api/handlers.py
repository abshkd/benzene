from piston.handler import BaseHandler
from piston.utils import rc
from django.contrib.auth.models import User

class UserHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = User
	fields = ('id', 'username', 'is_active', 'last_login', 'date_joined', ('profile', ('about', 'rank', 'avatar', 'donor')))
