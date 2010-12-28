from django.db import models
from django.contrib.auth.models import User
from manager import MessageManager
	
class Message(models.Model):
	content = models.TextField()
	subject = models.CharField(max_length = 80)
	sender = models.ForeignKey(User, related_name='outbox', null=True)
	recip = models.ForeignKey(User, related_name='inbox')
	time = models.DateTimeField(auto_now = True)
	thread_id = models.PositiveIntegerField()	# handle on SQL level?, says #django
	objects = MessageManager()
	
	def get_thread(self):
		return Message.objects.filter(thread_id = self.thread_id)
				
	def save(self):	#remove
		if not self.thread_id:
			try:
				self.thread_id = Message.objects.aggregate(models.Max('thread_id'))['thread_id__max']+1
			except TypeError: #first message
				self.thread_id = 1
		super(Message, self).save()

	class Meta:
		get_latest_by = 'time'
		ordering = ['-time']
