from django.db import models

class MessageManager(models.Manager):
	def try_latest(self):
		try:
			obj = super(MessageManager, self).latest()
		except DoesNotExist:
			return None