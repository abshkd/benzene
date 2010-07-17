import re
from django import forms
from models import  CustomUser, UnconfirmedUser
from utils import create_password

class RegForm(forms.Form):
	username = forms.CharField(max_length=20)
	email = forms.EmailField()
	email_again = forms.EmailField()
	password = forms.CharField(max_length=30, widget = forms.PasswordInput)
	password_again = forms.CharField(max_length=30, widget = forms.PasswordInput)
	
	def clean(self):
		cd = self.cleaned_data	
		if cd['email'] != cd['email_again']:
			raise forms.ValidationError("You entered 2 different emails")
		if cd['password'] != cd['password_again']:
			raise forms.ValidationError("You entered 2 different passwords")
		return cd
				
	def clean_email_again(self):
		email_again = self.cleaned_data['email_again']
		if CustomUser.objects.filter(email = email_again) or UnconfirmedUser.objects.filter(email = email_again):
			raise forms.ValidationError("An account already exists with this email")
		return email_again
		
	def clean_username(self):
		username = self.cleaned_data['username']
		p = re.compile('\w{,20}')
		if p.match(username).span() != (0, len(username)) or len(username)==0:
			raise forms.ValidationError("Only alphanumeric characters and underscore in the username please")	
		if CustomUser.objects.filter(username__iexact = username) or UnconfirmedUser.objects.filter(username__iexact = username):
			raise forms.ValidationError("Username already taken")
		return username
		
class ConfirmForm(forms.Form):
	confirmation_key = forms.CharField(max_length=26)
	
	def clean(self):
		cd = self.cleaned_data
		try:
			user = UnconfirmedUser.objects.get(identifier=cd['confirmation_key'])
			cd['unconfirmed'] = user
		except:
			raise forms.ValidationError("The confirmation key was not valid")
		return cd
	
class EditProfileForm(forms.Form):
	'''For every field (not including either of the password fields),
	there must be a field in CustomUser with the same name'''
	
	def __init__(self, *args, **kwargs): #must either pass 2 args or none
		if args:
			self.user = args[1]
			super(EditProfileForm, self).__init__(args[0], **kwargs)
		else:
			super(EditProfileForm, self).__init__(**kwargs)
	
	stylesheet = forms.URLField(required=False)
	avatar = forms.URLField(required=False)	
	about_text = forms.CharField(widget = forms.Textarea, required=False)
	email = forms.EmailField(required=False)
	old_password = forms.CharField(max_length=30, widget = forms.PasswordInput, required=False)
	new_password = forms.CharField(max_length=30, widget = forms.PasswordInput, required=False)
	new_password_again = forms.CharField(max_length=30, widget = forms.PasswordInput, required=False)
	
	def clean(self):
		result = {}
		cd = self.cleaned_data
		if cd.get('new_password') != cd.get('new_password_again'):
			raise forms.ValidationError('New passwords did not match')		
		if cd.get('new_password') or (cd.get('email') != self.user.email):
			if create_password(cd.get('old_password')) == self.user.password:
				if cd.get('new_password'):
					result['password'] = cd.get('new_password')
				else:
					result['email'] = cd.get('email')
			else:
				raise forms.ValidationError('Old password is not correct')
		del cd['email'], cd['old_password'], cd['new_password'], cd['new_password_again']
		for item in cd:
			result[item] = cd[item]			
		return result
		
		
		