from django.contrib import admin
from models import Forum, Thread, Post, LastRead, Profile

class ForumAdmin(admin.ModelAdmin):
	list_display = ('name', 'category')

class ThreadAdmin(admin.ModelAdmin):
	list_display = ('subject', 'forum')

class PostAdmin(admin.ModelAdmin):
	list_display = ('time', 'author', 'thread')

class LastReadAdmin(admin.ModelAdmin):
	list_display = ('thread', 'post', 'user')

admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LastRead, LastReadAdmin)
admin.site.register(Profile)
