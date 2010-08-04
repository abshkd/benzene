from models import Notification

def alert(users, notify_type, subject, url):
	'''Assesses whether or not a user's settings allow a notification, and creates a "smart link"
	notification if allowed
	'''
	
	users_permitting = (user for user in users if notify_type in user.notify_permissions)
	
	for user in users_permitting:
		n = Notification(recip=user, subject=subject, _url=url)
		n.save()