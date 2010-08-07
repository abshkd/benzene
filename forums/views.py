from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from base_utils import render_to_response
from models import Forum

@login_required
def index(request):
	forums = Forum.objects.all()
	categories = {}
	for f in forums:
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
