#userbase admin
from django.contrib import admin
from django.contrib.auth.models import User
from models import UnconfirmedUser
from piston.models import Consumer, Token
from django.contrib.sites.models import Site

class UnconfirmedUserAdmin(admin.ModelAdmin):
	list_display = ('email', 'username')

admin.site.register(UnconfirmedUser, UnconfirmedUserAdmin)
admin.site.register(Consumer)
admin.site.register(Token)

admin.site.unregister(Site)
