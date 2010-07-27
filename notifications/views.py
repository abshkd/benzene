from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.utils.hashcompat import md5_constructor
from models import Notification
from base_utils import render_to_response, multi_in_check

def delete_redirect(request)
	if not multi_in_check(request.GET, ('code', 'notification_id', 'link'))
		return HttpResonseNotFound()
	if md5_constructor(request.user.user_name) != request.GET['code']
		return HttpResponseNotFound()
	Notification.objects.get(id=request.GET['notification_id']).delete()
	return HttpResponseRedirect(request.GET['link'])
