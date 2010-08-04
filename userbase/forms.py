import re
from django import forms
from django.contrib.auth.models import User, check_password
from models import UnconfirmedUser

class RegForm(forms.Form):
	username = forms.CharField(max_length=20)
	email = forms.EmailField()
	email_again = forms.EmailField()
	password = forms.CharField(max_length=30, widget=forms.PasswordInput)
	password_again = forms.CharField(max_length=30, widget=forms.PasswordInput)
	invitation_key = forms.CharField(max_length=26, min_length=26, required=False, widget=forms.HiddenInput)
	
	def clean_email_again(self):
		email_again = self.cleaned_data['email_again']
		if User.objects.filter(email = email_again) or UnconfirmedUser.objects.filter(email = email_again):
			raise forms.ValidationError("An account already exists with this email")
		return email_again
		
	def clean_username(self):
		username = self.cleaned_data['username']
		p = re.compile('\w{,20}')
		if p.match(username).span() != (0, len(username)) or len(username)==0:
			raise forms.ValidationError("Only alphanumeric characters and underscore in the username please")	
		if User.objects.filter(username__iexact = username) or UnconfirmedUser.objects.filter(username__iexact = username):
			raise forms.ValidationError("Username already taken")
		return username

	def clean_invitation_key(self):
		if False:	# if registration is closed
			email = self.cleaned_data['email']
			invitation_key = self.cleaned_data['invitation_key']
			try:
				unconfirmed_user = UnconfirmedUser.objects.get(invitation_key=invitation_key)
			except:
				raise forms.ValidationError("The invitation key was not valid.")
			if email != unconfirmed_user.email:
				raise forms.ValidationError("The invitation key was not valid.")
			return invitation_key
		return username	
		
	def clean(self):
		cd = self.cleaned_data	
		if cd['email'] != cd['email_again']:
			raise forms.ValidationError("You entered 2 different emails")
		if cd['password'] != cd['password_again']:
			raise forms.ValidationError("You entered 2 different passwords")
		return cd

class ConfirmForm(forms.Form):
	confirmation_key = forms.CharField(max_length=26)
	
	def clean(self):
		cd = self.cleaned_data
		try:
			unconfirmed_user = UnconfirmedUser.objects.get(confirmation_key=cd['confirmation_key'])
			cd['unconfirmed'] = unconfirmed_user
		except:
			raise forms.ValidationError("The confirmation key was not valid.")
		return cd

class InviteForm(forms.Form):
	email = forms.EmailField()

class EditProfileForm(forms.Form):
	'''For every field (not including either of the password fields),
	there must be a field in User with the same name'''
	#if field isn't required (not counting passwords), it must have a default value
	
	def __init__(self, *args, **kwargs): #must either pass 2 args or none
		if args:
			self.user = args[1]
			super(EditProfileForm, self).__init__(args[0], **kwargs)
		else:
			super(EditProfileForm, self).__init__(**kwargs)
	
	stylesheet = forms.URLField(required=False)
	avatar = forms.URLField()
	about_text = forms.CharField(widget = forms.Textarea, required=False)
	email = forms.EmailField()
	old_password = forms.CharField(max_length=30, widget = forms.PasswordInput, required=False)
	new_password = forms.CharField(max_length=30, widget = forms.PasswordInput, required=False)
	new_password_again = forms.CharField(max_length=30, widget = forms.PasswordInput, required=False)
	
	def clean(self):
		result = {}
		cd = self.cleaned_data
		if cd.get('new_password') != cd.get('new_password_again'):
			raise forms.ValidationError('New passwords did not match')		
		if cd.get('new_password') or (cd.get('email') != self.user.email):
			if check_password(cd.get('old_password'), self.user.password):
				if cd.get('new_password'):
					result['password'] = create_password(cd.get('new_password'))
				else:
					result['email'] = cd.get('email')
			else:
				raise forms.ValidationError('Old password is not correct')
		del cd['email'], cd['old_password'], cd['new_password'], cd['new_password_again']
		for item in cd:
			result[item] = cd[item]			
		return result
