from django.core.management.base import BaseCommand, CommandError
from benzene.userbase.models import CustomUser, Rank

class Command(BaseCommand):
	help = 'Creates the first user (sysops) of a benzene-powered site'
	
	def handle(self, *args, **options):
		for rank in Rank.RANKS:
			k = Rank()
			k = rank
			k.save()
		email = raw_input('Email for sysop? ')
		username = raw_input('Username for sysop? ')
		password = raw_input('Password for sysop? ')
		pw_again = raw_input('Repeat your password ')
		sysop = CustomUser.objects.create_user(username, email, password)
		sysop.rank = 'SYS'
		sysop.save()
		