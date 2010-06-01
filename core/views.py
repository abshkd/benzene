# core views
import random

from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import RegForm
from models import CustomUser, UnconfirmedUser
import tools
import parts


def confirm(request, data):
	data = str(data)
	unconfirmed = UnconfirmedUser.objects.get(identifier=data)
	if unconfirmed:
		CustomUser.objects.create_user(unconfirmed.username, unconfirmed.email, unconfirmed.password)
		user = authenticate(username=unconfirmed.username, password=unconfirmed.password)
		unconfirmed.delete()
		login(request, user)
		return HttpResponseRedirect('/news/')
	else:
		return HttpResponse("FU Scammer")
		
def home(request):
	return render_to_response('visitor_home.html', {})

@login_required	
def news(request):
	return HttpResponse('This will be the news page')
	
def reg(request):
	if request.method == 'POST':
		form = RegForm(request.POST)
		if form.is_valid():
			emails_match = form.cleaned_data['email'] == form.cleaned_data['email_again']
			passwords_match = form.cleaned_data['password'] == form.cleaned_data['password_again']
			if emails_match and passwords_match:
				cd = form.cleaned_data
				data = tools.rand_str()
				u = UnconfirmedUser(username = cd['username'], email = cd['email'], password = cd['password'], identifier = data)
				u.save()
				send_mail('User Confirmation', data, 'noreply@example.com', [cd['email']])
				return HttpResponseRedirect('/success/')
	return render_to_response('registration.html', {'form' : RegForm()}, context_instance = RequestContext(request))


def success(request):
	return HttpResponse('Success!')
	
def test(request):
	return HttpResponse("woot")

def temphome(request):
	return render_to_response('temphome.html', context_instance = RequestContext(request))

def torrents(request):
	pass

def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")
		
	

		
	
