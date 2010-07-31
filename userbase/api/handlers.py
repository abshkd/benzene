from piston.handler import BaseHandler
from userbase.models import CustomUser

class CustomUserHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = CustomUser
	fields = ('id', 'username', 'is_active', 'last_login', 'date_joined', 'rank', 'donor', 'avatar', 'about_text')

	def read(self, request, username):
		return CustomUser.objects.get(username=username)
