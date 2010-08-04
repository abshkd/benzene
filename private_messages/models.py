from django.db import models
from django.contrib.auth.models import User
from manager import MessageManager
	
class Message(models.Model):
	content = models.TextField()
	subject = models.CharField(max_length = 80)
	sender = models.ForeignKey(User, related_name='outbox', null=True)
	recip = models.ForeignKey(User, related_name='inbox')
	time = models.DateTimeField(auto_now = True)
	objects = MessageManager()
	
	class Meta:
		get_latest_by = 'time'
		ordering = ['-time']

	def get_thread(self):
		return Message.objects.filter(models.Q(subject=self.subject), 
				(models.Q(sender=self.sender) & models.Q(recip=self.recip)) | 
				(models.Q(sender=self.recip) & models.Q(recip=self.sender)))
