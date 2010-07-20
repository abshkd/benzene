from django.core import mail
from django.contrib.auth.models import check_password
from django.test import TestCase
from forms import EditProfileForm
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
		
	def test_edit_profile(self):
		user = CustomUser.objects.create_user('user', 'user@example.com', 'abc123', already_hashed = False)
		
		#checks password hashing
		self.assertTrue(check_password('abc123', user.password)
		
		response = self.client.get('/profile/user/edit')
		self.assertEquals(response.status_code, 200)
		
		#need to complete later
		