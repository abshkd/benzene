from haystack.indexes import *
from haystack import site
from search_sites import get_index
from django.contrib.auth.models import User
from userbase.models import UserProfile

class UserIndex(get_index()):
	text = CharField(document=True, use_template=True, template_name='user_text.txt')

site.register(User, UserIndex)
