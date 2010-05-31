from django.db import models
from django.contrib.auth.models import User, UserManager

class CustomUser(User):
	avatar = models.URLField()
	passkey = models.CharField(max_length=50)
	stylesheet = models.URLField()
	objects = UserManager()

class UnconfirmedUser(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=128)
	email = models.EmailField()
	identifier = models.CharField(max_length=26)
