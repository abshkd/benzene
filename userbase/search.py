import solango
from models import CustomUser

class CustomUserDocument(solango.SearchDocument):
	user_name = solango.fields.CharField(indexed=True)
	e_mail = solango.fields.CharField(indexed=True)
	rank = solango.fields.CharField()
	donor = solango.fields.BooleanField()
	avatar = solango.fields.UrlField()
	invites = solango.fields.IntegerField()
	stylesheet = solango.fields.UrlField()
	about_text = solango.fields.TextField()
	
solango.register(CustomUser, CustomUserDocument)