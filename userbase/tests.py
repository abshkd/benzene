from django.core import mail
from django.test import TestCase
from models import UnconfirmedUser, CustomUser

class UserbaseTest(TestCase):
	def test_registration(self):
		self.client.post('/register/', {'username': 'user', 
							'email': 'user@example.com', 'email_again': 'user@example.com',
							'password': 'abc123', 'password_again': 'abc123'})
		
		#tests that 1 email has been sent
		self.assertEquals(len(mail.outbox), 1)
		
		#tests that email was sent to proper sender
		self.assertEquals(mail.outbox[0].to[0], 'user@example.com')
		
		#tests that UnconfirmedUser has a length of 1
		self.assertEquals(len(UnconfirmedUser.objects.all()), 1)
		
		#if confirmation email becomes more elaborate, code will break
		self.client.post('/confirm/', {'confirmation_key': mail.outbox[0].body})
		
		self.assertEquals(len(UnconfirmedUser.objects.all()), 0)
		self.assertEquals(len(CustomUser.objects.all()), 1)