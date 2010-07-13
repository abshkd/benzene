from django.contrib.auth.models import UserManager
from models import CustomUser
from utils import create_password

class CustomUserManager(UserManager):
	def create_user(self, username, email, password, already_hashed=True):
		'''Overrides create_user in UserManager to make denormalized schema more transparent.
		Password will normally be already hashed from user confirmation.
		
		'''
		if not already_hashed:
			password = create_password(password)
		c = CustomUser()
		c.username = username
		c.user_name = username
		c.email = email
		c.e_mail = email
		c.password = password
		c.save()
		return c