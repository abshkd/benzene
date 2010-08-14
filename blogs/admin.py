#blogs admin
from django.contrib import admin
from django.contrib.contenttypes import generic
from models import Blog, Post

class PostInline(generic.GenericTabularInline):
	model = Post
	ct_field = 'owner_type'
	ct_fk_field = 'owner_id'
	max_num = None

class BlogAdmin(admin.ModelAdmin):
	prepopulated_fields = {'name_slug': ('name',)}
	inlines = (PostInline,)
	
admin.site.register(Blog, BlogAdmin)
admin.site.register(Post)