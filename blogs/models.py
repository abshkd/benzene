from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Blog(models.Model):
	name = models.CharField(max_length=50, unique=True)
	name_slug = models.SlugField()
	posts = generic.GenericRelation('Post', content_type_field='owner_type', object_id_field='owner_id')
	
	def save(self):
		if not self.name_slug:
			self.name_slug = str(slugify(self.name))
		super(Blog, self).save()
	
	def __unicode__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=100, blank=True)
	content = models.TextField()
	author = models.ForeignKey(User, blank=True, null=True)
	time = models.DateTimeField(auto_now = True)
	owner_type = models.ForeignKey(ContentType)
	owner_id = models.PositiveIntegerField()
	owner = generic.GenericForeignKey('owner_type', 'owner_id')
	
	def __unicode__(self):
		return self.title
	
	class Meta(object):
		get_latest_by = 'time'
		ordering = ['-time']
