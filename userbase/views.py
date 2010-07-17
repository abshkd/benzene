import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import RegForm, ConfirmForm, EditProfileForm
from models import CustomUser, UnconfirmedUser
import utils
		
def confirm(request):
	form = ConfirmForm()
	if request.method == 'POST':
		form = ConfirmForm(request.POST)
		if form.is_valid():
			unconfirmed = form.cleaned_data['unconfirmed']
			new_user = CustomUser.objects.create_user(unconfirmed.username, unconfirmed.email, unconfirmed.password)
			unconfirmed.delete()
			utils.login_user(request, new_user)
			return HttpResponseRedirect('/profile/')
	return render_to_response('registration.html', {'form' : form}, context_instance = RequestContext(request))
	#registration template used on purpose, it is very generic, maybe 'confirm.html' template later if pages need to differ

@login_required		
def edit_profile(request, user_name):
	if request.method == 'GET':
		if user_name != request.user.user_name:
			return HttpResponseForbidden()
		user_data = {}
		for field in EditProfileForm():
			if 'password' not in field.name:
				user_data[field.name] = getattr(request.user, field.name)
		form = EditProfileForm(initial=user_data)
		return render_to_response('registration.html', {'form': form}, context_instance = RequestContext(request))
	else:
		form = EditProfileForm(request.POST, request.user)
		if form.is_valid():
			cd = form.cleaned_data
			for item in cd:
				if getattr(request.user, item) != cd[item]:
					setattr(request.user, item, cd[item])
			request.user.save()
		return HttpResponseRedirect('/profile/' + request.user.user_name)
		
def home(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	return render_to_response('visitor_home.html', {})
		
@login_required
def profile(request, user_name = ''):
	if not user_name:
		return HttpResponseRedirect('/profile/' + str(request.user.user_name))
	return render_to_response('internal.html', {'user': CustomUser.objects.get(user_name=user_name)})
	
def reg(request):
	form = RegForm()
	if request.method == 'POST':
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