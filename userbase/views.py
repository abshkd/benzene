import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from base_utils import render_to_response
from forms import RegForm, ConfirmForm, EditProfileForm
from models import CustomUser, UnconfirmedUser
import utils
import settings

def confirm(request, code=''):
	if request.method == 'GET' and code:
		form = ConfirmForm({'confirmation_key':code})
		if form.is_valid():
			unconfirmed = form.cleaned_data['unconfirmed']
			new_user = CustomUser.objects.create_user(unconfirmed.username, unconfirmed.email, unconfirmed.password)
			unconfirmed.delete()
			utils.login_user(request, new_user)
			return HttpResponseRedirect(reverse(profile, kwargs={'username':request.user.user_name}))
	return HttpResponse('The confirmation code was not valid')
		
@login_required
@csrf_protect
def edit_profile(request, username):
	if username != request.user.user_name:
		return HttpResponseForbidden()
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.user)
		if form.is_valid():
			cd = form.cleaned_data
			for item in cd:
				if getattr(request.user, item) != cd[item]:
					setattr(request.user, item, cd[item])
			request.user.save()
			return HttpResponseRedirect(reverse(profile, kwargs={'username':request.user.user_name}))
		else:
			return render_to_response(request, 'edit_profile.html', {'form': form})
	user_data = {}
	for field in EditProfileForm():
		if 'password' not in field.name:
			user_data[field.name] = getattr(request.user, field.name)
	form = EditProfileForm(initial=user_data)
	return render_to_response(request, 'edit_profile.html', {'form': form})
		
def home(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse(profile, kwargs={'username':request.user.user_name}))
	return render_to_response(request, 'visitor_home.html', {})
		
@login_required
def profile(request, username = ''):
	if not username:
		return HttpResponseRedirect(reverse(profile, kwargs={'username':request.user.user_name}))
	return render_to_response(request, 'profile.html', {'profile': CustomUser.objects.get(user_name=username)})

@csrf_protect
def reg(request):
	form = RegForm()
	if request.method == 'POST':
		form = RegForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			code = utils.rand_str()
			u = UnconfirmedUser(username = cd['username'], email = cd['email'],
				password = utils.create_password(cd['password']), identifier = code)
			u.save()
			send_mail('User Confirmation for ' + settings.SITE_NAME,
				render_to_string('confirmation_email.txt',
					{'code': code, 'site': settings.SITE_NAME, 'root': settings.SITE_ADDRESS }),
				'noreply@example.com', [cd['email']])
			request.session['email'] = cd['email']
			return HttpResponseRedirect('/success/')
	return render_to_response(request, 'registration.html', {'form' : form})
	
def success(request):
	try:
		email = request.session['email']
	except KeyError:
		return HttpResponse("You fail at succeeding.")
	return HttpResponse('A confirmation email was sent to ' + email)
