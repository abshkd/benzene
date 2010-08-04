from django.contrib.auth.models import User, UserManager
from django.db import models

RANKS = (
	('U', 'User'),
	('PU', 'Power User'),
	('E', 'Elite'),
	('VIP', 'VIP'),
	('MOD', 'Moderator'),
	('ADM', 'Administrator'),
	('SYS', 'Sysops'),
)	
					
class UserProfile(models.Model):			
	user = models.ForeignKey(User, unique=True)
	rank = models.CharField(max_length=3, choices=RANKS, default='U')
	donor = models.BooleanField(default=False)
	avatar = models.URLField(default='/static/avatars/default.png')
	invites = models.SmallIntegerField(default=0)
	about = models.TextField(blank=True)
	stylesheet = models.URLField(blank=True)
	
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
	username = models.CharField(max_length=20, unique=True, blank=True)
	inviter = models.ForeignKey(User, blank=True, null=True)
	email = models.EmailField(unique=True, db_index=True)
	confirmation_key = models.CharField(max_length=26, unique=True, blank=True)
	invitation_key = models.CharField(max_length=26, unique=True, blank=True)
	password = models.CharField(max_length=128, blank=True)
	expire = models.DateTimeField()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
