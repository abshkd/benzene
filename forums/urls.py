from django.conf.urls.defaults import *
from forums import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='forum_index'),
)
