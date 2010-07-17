from datetime import datetime
from django.contrib.auth.models import UserManager
from utils import create_password

class CustomUserManager(UserManager):
	def create_user(self, username, email, password, already_hashed=True):
		'''Overrides create_user in UserManager to make denormalized schema more transparent.
		Password will normally be already hashed from user confirmation.
		
		'''
		
		now = datetime.now()
		if not already_hashed:
			password = create_password(password)
		c = self.model()
		c.username = username
		c.user_name = username
		c.email = email
		c.password = password
		c.is_staff = False
		c.is_active = True
		c.is_superuser = False
		c.last_login = now
		c.date_joined = now
		c.save()
		return c