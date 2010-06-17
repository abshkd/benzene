import memcache

class QueuedSearchIndex(SearchIndex):
	q = Queue()
	def _setup_save(self, model):	
		q.add(model)
	
	def _setup_delete(self, model):
		q.add(model, delete=True)
		
class Queue(object):
	def __init__(self):
		mc = memcache.Client(['127.0.0.1:11211'], debug=0)
		#last_pos = self.get_last_pos()
	
	def add(self, model, delete=False):
		if delete:
			mc.set('queue_' + str(mc.get('queue_last')+1), (model.__class__name, model.id, 'delete'))
		else:
			mc.set('queue_' + str(mc.get('queue_last')+1), (model.__class__name, model.id))
		mc.incr('queue_last')
		
	'''def get_last_pos(self):
		if mc.get('queue_last') == -1 || mc.get('queue_last') == None:
			return -1
		else:
			k = 0
			while mc.get('queue_' + str(k)):
				k += 1
			return k-1'''
			
	def process(self):
		pass
		
'''RESUME LATER AFTER QUEUE FAIL'''