import re
from django import forms
from haystack.query import SearchQuerySet as sqs
from models import  CustomUser, UnconfirmedUser

class RegForm(forms.Form):
	email_again = forms.EmailField()
	email = forms.EmailField()
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=30, widget = forms.PasswordInput)
	password_again = forms.CharField(max_length=30, widget = forms.PasswordInput)
	
	def clean(self):
		cd = self.cleaned_data
		if sqs().models(CustomUser).filter(content__startswith=cd['username']).count() or UnconfirmedUser.objects.filter(username = cd['username']):
			raise forms.ValidationError("Username already taken")
		p = re.compile('\w{,20}')
		if p.match(cd['username']).span() != (0, len(cd['username'])) or len(cd['username'])==0:
			raise forms.ValidationError("Only alphanumeric characters and underscore in the username please")	
		if sqs().models(CustomUser).filter(content__startswith=cd['email']).count() or UnconfirmedUser.objects.filter(email = cd['email']):
			raise forms.ValidationError("An account already exists with this email")
		if cd['email'] != cd['email_again']:
			raise forms.ValidationError("You entered 2 different emails")
		if cd['password'] != cd['password_again']:
			raise forms.ValidationError("You entered 2 different passwords")
		return cd
		
class EditProfileForm(forms.Form):
	stylesheet = forms.URLField(required=False)
	avatar = forms.URLField(required=False)
	about_text = forms.CharField(required=False, widget=forms.Textarea)
	email = forms.EmailField(required=False)
	password = forms.CharField(required=False, max_length=30, widget=forms.PasswordInput)
	
	
	
