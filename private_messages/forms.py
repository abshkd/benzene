from django import forms
from userbase.models import CustomUser

class MessageForm(forms.Form):
	subject = forms.CharField(max_length=80)
	content = forms.CharField(widget = forms.Textarea)
	recip = forms.ModelChoiceField(queryset=CustomUser.objects, widget=forms.HiddenInput)
	thread_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
	
	