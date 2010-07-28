from django.contrib.auth.models import User, UserManager
from django.db import models
from manager import CustomUserManager

RANKS = (
	('U', 'User'),
	('PU', 'Power User'),
	('E', 'Elite'),
	('VIP', 'VIP'),
	('MOD', 'Moderator'),
	('ADM', 'Administrator'),
	('SYS', 'Sysops'),
		)	
					
class CustomUser(User):			
	user_name = models.CharField(max_length=20, unique=True)
	rank = models.CharField(max_length=3, choices=RANKS, default='U')
	donor = models.BooleanField(default=False)
	avatar = models.URLField(default='http://irregulartimes.com/smileyface125thumb.gif')
	invites = models.SmallIntegerField(default=0)
	about_text = models.TextField(blank=True)
	stylesheet = models.URLField(blank=True)
	objects = CustomUserManager()
	
	def save(self):
		if self.username != self.user_name:
			self.username = self.user_name
		super(CustomUser, self).save()
	
	def get_permissions(self):
		permissions = {}
		permissions['U'] = ['browse',]
		permissions['PU'] = permissions['U'].extend(['PU stuff'])
		permissions['E'] = permissions['PU'].extend([])
		permissions['VIP'] = permissions['E'].extend([])
		permissions['MOD'] = permissions['VIP'].extend([])
		permissions['ADM'] = permissions['MOD'].extend([])
		permissions['SYS'] = permissions['ADM'].extend([])
		return permissions[self.rank]
		
	def can(self, ability):
		return ability in self.get_permissions()

class UnconfirmedUser(models.Model):
	username = models.CharField(max_length=20, unique=True, db_index=True)
	password = models.CharField(max_length=128)
	email = models.EmailField(unique=True, db_index=True)
	identifier = models.CharField(max_length=26, unique=True)