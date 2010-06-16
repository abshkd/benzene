import from haystack.indexes import *
from haystack import site
from models import CustomUser

class CustomUserIndex(SearchIndex):
	text = CharField(document=True, user_template=True, template_name="customuser_text.txt")
	rank = CharField(model_attr='rank')
	donor = BooleanField(model_attr='donor')
	invites = IntegerField(model_attr='invites')

site.register(CustomUser, CustomUserIndex)