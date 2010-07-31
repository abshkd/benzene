from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.forms import HiddenInput
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.decorators.csrf import csrf_protect
from userbase.models import CustomUser
from forms import MessageForm
from models import Message
from utils import get_conversations
from base_utils import render_to_response

@login_required	
def inbox(request, outbox=False):
	if outbox:
		box_subjects = set(msg.subject for msg in request.user.outbox.all())
	else:
		box_subjects = set(msg.subject for msg in request.user.inbox.all())
	result = [conv for conv in get_conversations(request.user) if conv.subject in box_subjects]
	return render_to_response(request, 'inbox.html', {'conversations': result})

@login_required	
@csrf_protect
def view_conversation(request, key = ''):
	if key:
		for conv in get_conversations(request.user):
			if key == conv.key:
				form = MessageForm(initial={'subject': conv.subject, 'recip': conv.other_user.id})
				form.fields['subject'].widget = HiddenInput()
				return render_to_response(request, 'conversation.html', {'conversation': conv, 'form': form, 'other_user': conv.other_user})
	return HttpResponseNotFound()

@login_required
@csrf_protect
def new_conversation(request, recip=''):
	try:
		recip = CustomUser.objects.get(user_name=recip)
	except:
		return HttpResponseNotFound()
	return render_to_response(request, 'conversation.html', {'form': MessageForm(initial={'recip': recip.id}), 'other_user': recip})
	
@login_required
@csrf_protect
def send_message(request):
	if request.method != 'POST':
		return HttpResponseNotFound()
	form = MessageForm(request.POST)
	other_user = form['recip']
	if form.is_valid():
		cd = form.cleaned_data
		m = Message(sender=request.user, recip=cd['recip'], subject=cd['subject'], content=cd['content'])
		m.save()
		return HttpResponseRedirect(reverse('inbox'))
	return HttpResponse('There was an error with your message')
