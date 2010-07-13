import random
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
	algo = 'sha1'
	salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
	hsh = get_hexdigest(algo, salt, raw_pass)
	return '%s$%s$%s' % (algo, salt, hsh)