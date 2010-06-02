import solango
from models import CustomUser

class CustomUserDocument(solango.SearchDocument):
	user_name = solango.fields.CharField()
	
	def transform_username(self, instance):
		return instance.user_name
	
solango.register(CustomUser, CustomUserDocument)