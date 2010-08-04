from haystack.indexes import *
from haystack import site
from search_sites import get_index
from models import Message

class MessageIndex(get_index()):
	text = CharField(document=True, use_template=True, template_name='message_text.txt')
	subject = CharField(model_attr = 'subject')
	sender = CharField()
	recip = CharField()
	time = DateTimeField(model_attr = 'time')
	read = BooleanField(model_attr = 'read')
	
	def prepare_sender(self, obj):
		return obj.sender.username
		
	def prepare_recip(self, obj):
		return obj.recip.username
	
site.register(Message, MessageIndex)
