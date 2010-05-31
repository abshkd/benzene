# core views
import random

from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from models import CustomUser, UnconfirmedUser
from forms import RegForm

def confirm(request, data):
	data = str(data)
	user = UnconfirmedUser.objects.get(identifier=data)
	if user:
		CustomUser.objects.create_user(user.username, user.email, user.password)
		user.delete()
		return HttpResponseRedirect('/')
	else:
		return HttpResponse("FU Scammer")
		

def home(request):
	return render_to_response('visitor_home.html', {})
	
def reg(request):
	if request.method == 'POST':
		form = RegForm(request.POST)
		if form.is_valid():
			emails_match = form.cleaned_data['email'] == form.cleaned_data['email_again']
			passwords_match = form.cleaned_data['password'] == form.cleaned_data['password_again']
			if emails_match and passwords_match:
				cd = form.cleaned_data
				data = rand_str()
				u = UnconfirmedUser(username = cd['username'], email = cd['email'], password = cd['password'], identifier = data)
				u.save()
				send_mail('User Confirmation', data, 'noreply@example.com', [cd['email']])
				return HttpResponseRedirect('/success')
	return render_to_response('registration.html', {'form' : RegForm()})
	
def success(request):
	return HttpResponse('Success!')
	
def test(request):
	return HttpResponse("woot")
	
def rand_str():
	string = ''
	set = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
	for character in range(random.randint(15,25)):
		string += random.choice(set)
	return string
		
	