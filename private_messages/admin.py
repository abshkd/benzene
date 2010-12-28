#private_messages admin
from django.contrib import admin
from models import Message

class MessageAdmin(admin.ModelAdmin):
	list_display = ('subject', 'sender', 'recip', 'thread_id')

admin.site.register(Message, MessageAdmin)
