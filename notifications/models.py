from urllib import urlencode
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.hashcompat import md5_constructor
from django.contrib.auth.models import User

class Notification(models.Model):
	subject = models.CharField(max_length = 120)
	_url - models.URLField()
	recip = models.ForeignKeyField(User)
	time = models.DateTimeField(auto_now = True)
	
	def __getattr__(self, name):
		if name == 'url':
			url = reverse('handle_notification')
			url += '?' + urlencode({'notification_id': self.id, 
				'link': self._url,
				'code': md5_constructor(self.recip.user_name).hexdigest()})
			return url
		else:
			super(Notification, self).__getattr__(name)
	
	class Meta:
		get_latest_by = 'time'
		ordering = ['-time']
