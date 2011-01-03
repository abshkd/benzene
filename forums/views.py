from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from base_utils import render_to_response
from models import Forum, Thread, Post, LastRead
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from forms import PostForm
from django.forms import HiddenInput

@login_required
def index(request):
	forums = Forum.objects.all()
	categories = {}
	for f in forums:
		print f.id
		print forums
		if f.category in categories:
			categories[f.category].append(f)
		else:
			categories[f.category] = [f]
		#for c in categories:
			#if f.category == c['name']:
				#c['forums'].append(f)
				#break
		#categories.append({'name': f.category, 'forums': [f]})
	cats = []
	for name, forums in categories.items():
		cats.append({'name': name, 'forums': forums})
	return render_to_response(request, 'index.html', {'categories': cats})

@login_required
def forum(request, forum_id):
	forum_id = int(forum_id)
	forum = Forum.objects.get(id=forum_id)
	threads_per_page = 50	# this should be a lookup to userprofile
	paginator = Paginator(Thread.objects.filter(forum=forum_id), threads_per_page)
	page = int(request.GET.get('page', 1))
	try:
		threads = paginator.page(page)
	except (EmptyPage, InvalidPage):
		threads = paginator.page(paginator.num_pages)
	return render_to_response(request, 'forum.html', {'forum': forum, 'threads': threads})

@login_required
@csrf_protect
def thread(request, thread_id):
	thread = Thread.objects.get(id=thread_id)
	posts_per_page = 5	# this should be a lookup to userprofile
	paginator = Paginator(Post.objects.filter(thread=thread_id).order_by('time'), posts_per_page)
	page = int(request.GET.get('page', 1))

	if thread_id: thread_id = int(thread_id)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			p = Post(content=cd['content'], author=request.user, thread=thread)
			p.save()
			page = paginator.num_pages
		else:
			return HttpResponse('Error posting; post form was not valid.')

	try:
		posts = paginator.page(page)
	except (EmptyPage, InvalidPage):
		posts = paginator.page(paginator.num_pages)

	last_post = posts.object_list[len(posts.object_list)-1]
	try:
		lr = LastRead.objects.get(thread=thread, user=request.user)
		if lr.post.id < last_post.id:
			lr.post = last_post
			lr.save()
		else:
			last_post = lr.post
	except:
		lr = LastRead(thread=thread, user=request.user, post=last_post)
		lr.save()

	form = PostForm()
	return render_to_response(request, 'thread.html', {'thread': thread, 'posts': posts, 'form': form, 'last_read': last_post})
