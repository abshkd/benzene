#private_messages admin
from django.contrib import admin
from models import Message

class MessageAdmin(admin.ModelAdmin):
	list_display = ('subject', 'sender', 'recip')

admin.site.register(Message, MessageAdmin)
