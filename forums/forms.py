from django import forms
from models import Thread, Post

class PostForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea)
