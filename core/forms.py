from django import forms

class RegForm(forms.Form):
	email = forms.EmailField()
	email_again = forms.EmailField()
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=30, widget = forms.PasswordInput)
	password_again = forms.CharField(max_length=30, widget = forms.PasswordInput)