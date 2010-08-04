def login_user(request, user):
	"""
	Log in a user without requiring creditials (using ``login`` from
	``django.contrib.auth``, first finding a matching backend).
	Source is http://djangosnippets.org/snippets/1547/
	"""
	from django.contrib.auth import load_backend, login
	import settings
	if not hasattr(user, 'backend'):
		for backend in settings.AUTHENTICATION_BACKENDS:
			if user == load_backend(backend).get_user(user.pk):
				user.backend = backend
				break
	if hasattr(user, 'backend'):
		return login(request, user)
