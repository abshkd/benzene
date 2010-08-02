#userbase admin
from django.contrib import admin
from django.contrib.auth.models import User
from models import CustomUser, UnconfirmedUser
from piston.models import Consumer, Token
from django.contrib.sites.models import Site

class CustomUserAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	fields = ('user_name', 'email', 'is_active', 'is_staff', 'is_superuser',
				'last_login', 'date_joined', 'rank', 'donor', 'avatar', 'invites',
				'about_text', 'groups', 'user_permissions',)
	
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UnconfirmedUser)
admin.site.register(Consumer)
admin.site.register(Token)

admin.site.unregister(User)
admin.site.unregister(Site)