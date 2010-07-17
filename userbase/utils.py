from datetime import datetime
import random
from django.db import models
from django.utils import simplejson as json
from django.conf import settings
from django.contrib.auth.models import get_hexdigest

def rand_str(lower=15,upper=25,fixed=0):
	string = ''
	set = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
	if fixed != 0:
		num_characters = fixed
	else:
		num_characters = random.randint(lower,upper)
	for character in xrange(num_characters):
		string += random.choice(set)
	return string
	
def create_password(raw_pass):
	'''Changes a raw password into a hashed password'''
	algo = 'sha1'
	salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
	hsh = get_hexdigest(algo, salt, raw_pass)
	return '%s$%s$%s' % (algo, salt, hsh)
	
def login_user(request, user):
    """
    Log in a user without requiring credentials (using ``login`` from
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