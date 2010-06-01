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


def confirm(request, data):
	data = str(data)
	unconfirmed = UnconfirmedUser.objects.get(identifier=data)
	if unconfirmed:
		CustomUser.objects.create_user(unconfirmed.username, unconfirmed.email, unconfirmed.password)
		user = authenticate(username=unconfirmed.username, password=unconfirmed.password)
		unconfirmed.delete()
		login(request, user)
		return HttpResponseRedirect('/profile/')
	else:
		return HttpResponse("FU Scammer")

@login_required		
def edit_profile(request):
	return HttpResponse("Make form, complete later")
		
def home(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	return render_to_response('visitor_home.html', {})
	
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
	
@login_required
def profile(request, uid = 0):
	if uid == 0:
		uid = request.user.id
	return HttpResponse(CustomUser.objects.get(id=uid).username)
	
def reg(request):
	form = RegForm()
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
				request.session['email'] = cd['email']
				return HttpResponseRedirect('/success/')
			else:
				form.errors.append('Your emails or passwords do not match')
	return render_to_response('registration.html', {'form' : form}, context_instance = RequestContext(request))

def rand_str():
	string = ''
	set = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
	for character in range(random.randint(15,25)):
		string += random.choice(set)
	return string
	
def success(request):
	try:
		email = request.session['email']
	except KeyError:
		return HttpResponse("You fail at succeeding.")
	return HttpResponse('A confirmation email was sent to ' + email)
	
def test(request):
	return HttpResponseRedirect("/")
	

		
	