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
