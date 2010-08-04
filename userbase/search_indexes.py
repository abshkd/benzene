from haystack.indexes import *
from haystack import site
from search_sites import get_index
from django.contrib.auth.models import User

class UserIndex(get_index()):
	text = CharField(document=True, use_template=True, template_name='user_text.txt')
#	rank = CharField(model_attr='rank')
#	donor = BooleanField(model_attr='donor')
#	invites = IntegerField(model_attr='invites')

site.register(User, UserIndex)
