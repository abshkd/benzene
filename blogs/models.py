from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from userbase.models import CustomUser

class Blog(models.Model):
	name = models.CharField(max_length=50, unique=True)
	posts = generic.GenericRelation('Post', content_type_field='owner_type', object_id_field='owner_id')

class Post(models.Model):
	title = models.CharField(max_length=100, blank=True)
	content = models.TextField()
	author = models.ForeignKey(CustomUser, blank=True)
	time = models.DateTimeField(auto_now = True)
	owner_type = models.ForeignKey(ContentType)
	owner_id = models.PositiveIntegerField()
	owner = generic.GenericForeignKey('owner_type', 'owner_id')
	
	class Meta(object):
		get_latest_by = 'time'
		ordering = ['-time']