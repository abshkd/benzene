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
import utils

def confirm(request, code):
	code = str(code)
	unconfirmed = UnconfirmedUser.objects.get(identifier=code)
	if unconfirmed:
		new_user = CustomUser.objects.create_user(unconfirmed.username, unconfirmed.email, unconfirmed.password)
		unconfirmed.delete()
		utils.login_user(request, new_user)
		return HttpResponseRedirect('/profile/')
	else:
		return HttpResponse("Sorry, you confirmation code doesn't exist")

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
def profile(request, user_name = ''):
	if not user_name:
		return HttpResponseRedirect('/profile/' + str(request.user.user_name))
	return render_to_response('internal.html', {'user': CustomUser.objects.get(user_name=user_name)})
	
def reg(request):
	form = RegForm()
	if request.method == 'POST':
		x = request.POST
		form = RegForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			code = utils.rand_str()
			u = UnconfirmedUser(username = cd['username'], email = cd['email'], password = utils.create_password(cd['password']), identifier = code)
			u.save()
			send_mail('User Confirmation', code, 'noreply@example.com', [cd['email']])
			request.session['email'] = cd['email']
			return HttpResponseRedirect('/success/')
	return render_to_response('registration.html', {'form' : form}, context_instance = RequestContext(request))

def torrents_view(request):
	return render_to_response('internal.html', {})
	
def success(request):
	try:
		email = request.session['email']
	except KeyError:
		return HttpResponse("You fail at succeeding.")
	return HttpResponse('A confirmation email was sent to ' + email)
	
def test(request):
	return HttpResponseRedirect("/")


	

		
	
