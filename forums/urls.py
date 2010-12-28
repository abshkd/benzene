from django.conf.urls.defaults import *
from forums import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='forum_index'),
	url(r'^(?P<forum_id>\d*)/$', views.forum, name='view_forum'),
	url(r'^thread/(?P<thread_id>\d*)/$', views.thread, name='view_thread'),
)
