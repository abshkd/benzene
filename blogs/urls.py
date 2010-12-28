#blogs urls
from django.conf.urls.defaults import *
from blogs import views

urlpatterns = patterns('',
	url(r'^(?P<name_slug>[\w\-]{,50})/$', views.blog_view, name='blog_view'),
)