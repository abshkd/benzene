from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
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
	for conv in result:
		print conv.__dict__.keys()
	return render_to_response(request, 'inbox.html', {'conversations': result})

@login_required	
def view_conversation(request, key = ''):
	if key:
		for conv in get_conversations(request.user):
			if key == conv.key:
				return render_to_response('some_other_template', {'conversation': conv})
	return HttpResponseNotFound()
	
@login_required
def send_message(request, recip=''):
	try:
		recip_instance = CustomUser.objects.get(user_name=recip)
	except:
		return HttpResponseNotFound()
	form = MessageForm()
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			m = Message(sender=request.user, recip=recip_instance, subject=cd['subject'], content=cd['content'])
			m.save()
			return HttpResponseRedirect(reverse('inbox'))
	return render_to_response(request, 'send_message.html', {'form': form, 'other_user': recip_instance})
		