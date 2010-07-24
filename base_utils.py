from django import shortcuts
from django.template import RequestContext

def render_to_response(request, *args, **kwargs):
	return shortcuts.render_to_response(*args, context_instance=RequestContext(request), **kwargs)