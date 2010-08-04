import random
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, UserManager
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from base_utils import render_to_response
from forms import RegForm, ConfirmForm, EditProfileForm
from models import UserProfile, UnconfirmedUser
import settings
from utils import login_user

def confirm(request, code=''):
	if request.method == 'GET' and code:
		form = ConfirmForm({'confirmation_key':code})
		if form.is_valid():
			unconfirmed = form.cleaned_data['unconfirmed']
			new_user = User.objects.create_user(unconfirmed.username, unconfirmed.email, unconfirmed.password)
#user_profile = UserProfile(user=new_user)	# hack, see docs
#user_profile.save()
			new_user.save()
			unconfirmed.delete()
			login_user(request, new_user)
			return HttpResponseRedirect(reverse(profile, kwargs={'username': request.user.username}))
	return HttpResponse('The confirmation code was not valid.')
		
@login_required
@csrf_protect
def edit_profile(request, username):
	if username != request.user.username:
		return HttpResponseForbidden()
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.user)
		if form.is_valid():
			cd = form.cleaned_data
			for item in cd:
				if getattr(request.user, item) != cd[item]:
					setattr(request.user, item, cd[item])
			request.user.save()
			return HttpResponseRedirect(reverse(profile, kwargs={'username': request.user.username}))
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
		return HttpResponseRedirect(reverse(profile, kwargs={'username': request.user.username}))
	return render_to_response(request, 'visitor_home.html', {})
		
@login_required
def profile(request, username = ''):
	if not username:
		return HttpResponseRedirect(reverse(profile, kwargs={'username': request.user.username}))
	return render_to_response(request, 'profile.html', {'profile': User.objects.get(username=username)})

@csrf_protect
def reg(request, code=''):
	if request.method == 'POST':
		print "post"
		form = RegForm(request.POST)
		print "post-"
		if form.is_valid():
			print "valid"
			cd = form.cleaned_data
			ck = User.objects.make_random_password(length=26)
			u = UnconfirmedUser(username=cd['username'], email=cd['email'],
				password=cd['password'], confirmation_key=ck,
				expire=datetime.datetime.now() + datetime.timedelta(days=3))
			u.save()
			send_mail('User Confirmation for ' + settings.SITE_NAME, render_to_string('confirmation_email.txt',
				{'key': ck, 'site': settings.SITE_NAME, 'root': settings.SITE_ADDRESS }),
				'noreply@example.com', [cd['email']])
			request.session['email'] = cd['email']
			print "return"
			return HttpResponseRedirect('/success/')
		else:
			print "not"
	elif request.method == 'GET':
		print "get"
		if True:	# Registration is open
			form = RegForm()
			return render_to_response(request, 'registration.html', {'form': form})
		elif code:
			try:
				uu = UnconfirmedUser.objects.get(invitation_key=code)
				form = RegForm(initial={'invitation_key': code, 'email': uu.email})
				if form.is_valid():
					return render_to_response(request, 'registration.html', {'form': form})
				return HttpResponseRedirect('/')
			except:
				return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/')
	print "neither"
	return HttpResponseRedirect('/')

@login_required
@csrf_protect
def invite(request):
	form = InviteForm()
	if request.method == 'POST':
		form = InviteForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			invitation_key = User.objects.make_random_password(length=26)
			u = UnconfirmedUser(email=cd['email'], invitation_key=invitation_key,
				expire=datetime.datetime.now() + datetime.timedelta(days=3))
			u.save()
			send_mail('You have been invited to ' + settings.SITE_NAME, render_to_string('invitation_email.txt',
				{'key': invitation_key, 'email': email, 'site': settings.SITE_NAME, 'root': settings.SITE_ADDRESS }),
				'noreply@example.com', [cd['email']])
			return HttpResponseRedirect('/invite/')
	return render_to_response(request, 'invite.html', {'form': form })
	
def success(request):
	try:
		email = request.session['email']
	except KeyError:
		return HttpResponse("You fail at succeeding.")
	return HttpResponse('A confirmation email was sent to ' + email)
