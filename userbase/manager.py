from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
	def create_user(self, username, email, password=None):
		user = UserManager.create_user(self, username, email, password)
		user.user_name = username
		user.e_mail = email
		user.save()
		return user