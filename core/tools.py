def rand_str():
	string = ''
	set = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
	for character in range(random.randint(15,25)):
		string += random.choice(set)
	return string
