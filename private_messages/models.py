from django.db import models
from userbase.models import CustomUser
	
class Message(models.Model):
	content = models.TextField()
	subject = models.CharField(max_length = 80)
	sender = models.ForeignKey(CustomUser, related_name='outbox')
	recip = models.ForeignKey(CustomUser, related_name = 'inbox')
	read = models.BooleanField(default=False)
	time = models.DateTimeField(auto_now = True)
	
	class Meta:
		get_latest_by = 'time'
		ordering = ['-time']