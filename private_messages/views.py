vfrom django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.datastructures import SortedDict
from forms import MessageForm
from models import Message
from userbase.models import CustomUser

@login_required
def inbox(request):
	convs = SortedDict()
	messages = request.user.inbox.all() + request.user.outbox.all()
	messages.sort(key=lambda msg: msg.time, reverse=True)
	inbox_subjects = set(msg.subject for msg in request.user.inbox.all())
	for msg in messages:
		if msg.subject in inbox_subjects:
			convs[msg.subject].append(msg)
		else:
			convs[msg.subject] = [msg]
	convs = convs.values()
		
	
	
