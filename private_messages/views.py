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
	messages = []
	if outbox:
		box_thread_ids = set(msg.thread_id for msg in request.user.outbox.all())
		for msg in request.user.outbox.all():
			if msg.thread_id in box_thread_ids:
				messages.append(msg)
				box_thread_ids.discard(msg.thread_id)
	else:
		box_thread_ids = set(msg.thread_id for msg in request.user.inbox.all())
		for msg in request.user.inbox.all():
			if msg.thread_id in box_thread_ids:
				messages.append(msg)
				box_thread_ids.discard(msg.thread_id)
	return render_to_response(request, 'inbox.html', {'conversations': messages})

@login_required	
@csrf_protect
def view_conversation(request, thread_id=''):
	thread_id = int(thread_id)
	if thread_id:
		conv = Message.objects.filter(thread_id=thread_id)
		last = conv.latest()
		if last.sender == request.user:
			other_user = last.recip.id
			form = MessageForm(initial={'subject': last.subject, 'recip': last.recip.id, 'thread_id': thread_id})
		elif last.recip == request.user:
			other_user = last.sender.id
			form = MessageForm(initial={'subject': last.subject, 'recip': last.sender.id, 'thread_id': thread_id})
		else:
			return HttpResponseNotFound()
		form.fields['subject'].widget = HiddenInput()
		return render_to_response(request, 'conversation.html', {'conversation': conv, 'form': form, 'other_user': other_user})
	return HttpResponseNotFound()

@login_required
@csrf_protect
def new_conversation(request, recip=''):
	try:
		recip = CustomUser.objects.get(username=recip)
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
		m = Message(sender=request.user, recip=cd['recip'], subject=cd['subject'], content=cd['content'], thread_id=cd.get('thread_id'))
		m.save()
		return HttpResponseRedirect(reverse('inbox'))
	return HttpResponse('There was an error with your message')
