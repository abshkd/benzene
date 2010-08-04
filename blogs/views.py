from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contirb.auth.models import User
from base_utils import render_to_response
from models import Blog

@login_required
def blog_view(request, blog_name='news'):
	blog = Blog.objects.select_related(depth=2).get(name_slug=blog_name)
	return render_to_response(request, 'blog_overview.html', {'blog': blog})
	
@login_required
def view_post(request, blog_name='news', post_date=''):
	pass
	#code later
