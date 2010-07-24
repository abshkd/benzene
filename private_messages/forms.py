from django import forms

class MessageForm(forms.Form):
	subject = forms.CharField(max_length=80)
	content = forms.CharField(widget = forms.Textarea)
	
	