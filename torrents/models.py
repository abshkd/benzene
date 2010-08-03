from django.db import models

class Torrent(models.Model):
	name = models.CharField(max_length=180)
	data = models.TextField()
	time_uploaded = models.DateTimeField(auto_now=True)
