from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from userbase.models import CustomUser
from base_utils import render_to_response
from models import Blog

@login_required
def overview(request, blog_name='news'):
	blog = Blog.objects.select_related(depth=2).get(name=blog_name)
	return render_to_response(request, 'blog_overview.html', {'blog': blog})
	
@login_required
def view_post(request, blog_name='news', post_date=''):
	pass
	#code later