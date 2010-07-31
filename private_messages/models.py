from django.db import models
from userbase.models import CustomUser
from manager import MessageManager
	
class Message(models.Model):
	content = models.TextField()
	subject = models.CharField(max_length = 80)
	sender = models.ForeignKey(CustomUser, related_name='outbox', null=True)
	recip = models.ForeignKey(CustomUser, related_name = 'inbox')
	time = models.DateTimeField(auto_now = True)
	objects = MessageManager()
	
	class Meta:
		get_latest_by = 'time'
		ordering = ['-time']

	def get_thread(self):
		return Message.objects.filter(models.Q(subject__exact=self.subject), 
				(models.Q(sender__exact=self.sender) & models.Q(recip__exact=self.recip)) | 
				(models.Q(sender__exact=self.recip) & models.Q(recip__exact=self.sender)))
