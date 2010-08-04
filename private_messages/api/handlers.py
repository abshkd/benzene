from piston.handler import BaseHandler
from piston.utils import rc
from private_messages.models import Message
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class MessageHandler(BaseHandler):
	allowed_methods = ('GET', 'POST')
	model = Message
	fields = ('subject', 'time', ('sender', ('username',)), ('recip', ('username',)), 'content')

	def read(self, request, id=None):
		if id:
			try:
				m = Message.objects.get(id=id)
				if m.sender.username == request.user.username or m.recip.username == request.user.username:
					return m.get_thread()
				else:
					return rc.FORBIDDEN
			except ObjectDoesNotExist:
				return rc.NOT_FOUND
		else:
			m = list(request.user.inbox.all())
			m.extend(request.user.outbox.all())
			return m
	
	def create(self, request):
		d = self.flatten_dict(request.POST)
		if 'recip' in d and 'subject' in d and 'content' in d:
			try:
				m = Message(sender=request.user,
					recip=User.objects.get(username=d['recip']),
					subject=d['subject'], content=d['content'])
				m.save()
				return rc.CREATED
			except:
				return rc.BAD_REQUEST
		else: 
			return rc.BAD_REQUEST
