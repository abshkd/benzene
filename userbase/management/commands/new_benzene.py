from django.core.management.base import BaseCommand, CommandError
from userbase.models import CustomUser
from userbase.forms import RegForm

class Command(BaseCommand):
	args = ''
	help = 'Creates the first user (sysops) of a benzene-powered site'
	
	def handle(self, *args, **options):
		reg = {}
		reg['username'] = raw_input('Username for sysop? ')
		reg['email'] = raw_input('Email for sysop? ')
		reg['email_again'] = raw_input('Email again? ')
		reg['password'] = raw_input('Password for sysop? ')
		reg['password_again'] = raw_input('Password again? ')
		form = RegForm(reg)
		if form.is_valid() and not len(CustomUser.objects.all()):
			sysop = CustomUser.objects.create_user(reg['username'], reg['email'], reg['password'], already_hashed = False)
			sysop.rank = 'SYS'
			sysop.save()
		else:
			 self.stdout.write('There were errors in your data. Please try again')
		
		