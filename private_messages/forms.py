from django import forms
from userbase.models import CustomUser

class MessageForm(forms.Form):
	subject = forms.CharField(max_length=80)
	content = forms.CharField(widget = forms.Textarea)
	recip = forms.ModelChoiceField(queryset=CustomUser.objects)
	
	