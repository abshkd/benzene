from django.db import models

class Poll(models.Model):
	description = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.description

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	description = models.CharField(max_length=100)
	votes = models.IntegerField()

	def __unicode__(self):
		return self.description
