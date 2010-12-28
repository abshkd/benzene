from django.db import models
from django.contrib.auth.models import User
from benzene.polls.models import Poll

class Forum(models.Model):
	name = models.CharField(max_length=50)
	category = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Thread(models.Model):
	subject = models.CharField(max_length=100)
	forum = models.ForeignKey(Forum)
	locked = models.BooleanField()
	poll = models.ForeignKey(Poll, blank=True, null=True)

	def __unicode__(self):
		return self.subject

class Post(models.Model):
	content = models.TextField()
	time = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User)
	thread = models.ForeignKey(Thread)

	def __unicode__(self):
		return self.content

	class Meta(object):
		get_latest_by = 'time'
		ordering = ['-time']
