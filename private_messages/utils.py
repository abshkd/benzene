try:
	import cPickle as pickle
except:
	import pickle
from django.core.cache import cache
from django.utils.hashcompat import md5_constructor
from models import Message

class Conversation(object):
	def __init__(self, subject, other_user):
		self.subject = subject
		self.other_user = other_user
		self.messages = []
		self.key = md5_constructor(subject + other_user.user_name).hexdigest()
	
	def __eq__(self, other):
		if hasattr(other, 'key'):
			return self.key == other.key
		return False
	
	def __getattr__(self, name):
		if name == 'time':
			if len(self.messages):
				return max(msg.time for msg in self.messages)
			else:
				raise ValueError('Conversation must have messages to have a time')
		else:
			raise AttributeError(name)
			
def update_conversations(username, conversations, messages):
	conversations = conversations[:]
	for msg in messages:
		if msg.sender.user_name == username:
			conv = Conversation(msg.subject, msg.recip)
		else:
			conv = Conversation(msg.subject, msg.sender)
		if conv in conversations:
			index = conversations.index(conv)
			conversations[index].messages.insert(0, msg)
			conversations.insert(0, conversations.pop(index))
		else:
			conv.messages.insert(0, msg)
			conversations.insert(0, conv)
	return conversations
	
def get_messages(user):
	messages = list(user.inbox.all())
	messages.extend(user.outbox.all())
	messages.sort(key=lambda msg: msg.time)
	return messages
	
def get_conversations(user):
	convs_pickle = cache.get(user.user_name + '_convs')
	if convs_pickle and pickle.loads(convs_pickle):
		convs = pickle.loads(convs_pickle)
		latest_in = user.inbox.try_latest()
		latest_out = user.outbox.try_latest()
		if latest_in and latest_out and (latest_in.time > convs[0].time or latest_out.time > convs[0].time): #if update is needed
			messages = get_messages(user)	
			updates = []
			for msg in messages[::-1]:
				if msg.time > convs[0].time:
					updates.insert(0, msg)
				else:
					break		
			convs = update_conversations(user.user_name, convs, updates)
		cache.set(user.user_name + '_convs', pickle.dumps(convs), 60*15)
		return convs
	else:
		messages = get_messages(user)
		convs = update_conversations(user.user_name, [], messages)
		cache.set(user.user_name + '_convs', pickle.dumps(convs), 60*15)
		return convs
