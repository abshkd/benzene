from django.db import models
from django.contrib.auth.models import User, UserManager

class Rank(models.Model):
	'''One of each rank will be in the database, and each rank will have its own set of permissions
	which will each be a boolean field'''
	#possibility: implement rank as dictionary literal in code rather than db entries
	
	RANKS = (
		('U', 'User'),
		('PU', 'Power User'),
		('E', 'Elite'),
		('VIP', 'VIP'),
		('MOD', 'Moderator'),
		('ADM', 'Administrator'),
		('SYS', 'Sysops'),
			)	
			
	rank = models.CharField(max_length=3, choices=RANKS, default='U')
	
	def __get__(self, instance, owner):
		return instance.rank
		
	def __set__(self, instance, value): 
		for pair in RANKS:
			if value in pair:
				instance.rank = pair[0]
				return True #put in function call to update permissions here
		#raise error here because value isn't valid rank
	
class Preferences(models.Model):
	stylesheet = models.URLField()	
	
class CustomUserManager(UserManager):
	def create_user(self, username, email, password=None):
		UserManager.create_user(self, username, email, password)
		user = authenticate(username=unconfirmed.username, password=unconfirmed.password)
		user.user_name = username
		user.e_mail = email
		user.save()
				
class CustomUser(User):	
	user_name = models.CharField(max_length=20, unique=True)
	e_mail = models.EmailField(unique=True)
	rank = models.ForeignKey(Rank)
	donor = models.BooleanField(default=False)
	avatar = models.URLField(default='http://irregulartimes.com/smileyface125thumb.gif')
	invites = models.SmallIntegerField(default=0)
	preferences = models.OneToOneField(Preferences)
	about_text = models.TextField()
	objects = CustomUserManager()

class UnconfirmedUser(models.Model):
	username = models.CharField(max_length=20, unique=True, db_index=True)
	password = models.CharField(max_length=128)
	email = models.EmailField(unique=True, db_index=True)
	identifier = models.CharField(max_length=26, unique=True)
	



			

	