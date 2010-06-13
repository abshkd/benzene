import re

from django import forms

from models import  CustomUser, UnconfirmedUser
from solango import connection

class RegForm(forms.Form):
	email = forms.EmailField()
	email_again = forms.EmailField()
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=30, widget = forms.PasswordInput)
	password_again = forms.CharField(max_length=30, widget = forms.PasswordInput)
	
	def clean(self):
		cd = self.cleaned_data
		if cd['email'] != cd['email_again']:
			raise forms.ValidationError("You entered 2 different emails")
		if cd['password'] != cd['password_again']:
			raise forms.ValidationError("You entered 2 different passwords")
		return cd
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if connection.select(user_name = username).count or UnconfirmedUser.objects.filter(username = username):
			raise forms.ValidationError("Username already taken")
		p = re.compile('\w{,20}')
		if p.match(username).span() != (0, len(username)) or len(username)==0:
			raise forms.ValidationError("Only alphanumeric characters and underscore in the username please")	
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if connection.select(e_mail = email).count or UnconfirmedUser.objects.filter(email = email):
			raise forms.ValidationError("An account already exists with this email")
		return email
		
class EditProfileForm(forms.Form):
	stylesheet = forms.URLField(required=False)
	avatar = forms.URLField(required=False)
	about_text = forms.CharField(required=False, widget=forms.TextField)
	email = forms.EmailField(required=False)
	password = forms.CharField(required=False, max_length=30, widget=forms.PasswordInput)
	
	
	