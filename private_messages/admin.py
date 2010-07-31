#private_messages admin
from django.contrib import admin
from models import Message

class CustomMessage(admin.ModelAdmin):
	list_display = ('subject', 'sender', 'recip')

admin.site.register(Message, CustomMessage)
