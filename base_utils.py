from django import shortcuts
from django.template import RequestContext

def render_to_response(request, *args, **kwargs):
	return shortcuts.render_to_response(*args, context_instance=RequestContext(request), **kwargs)
	
def hasattrs(obj, attrs):
	for attribute in attrs:
		if not hasattr(obj, attribute):
			return False
	return True
	
def multi_in_check(obj, keys):
	for key in keys:
		if not key in obj:
			return False
	return True