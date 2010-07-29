import haystack
from haystack.indexes import RealTimeSearchIndex
from settings import DEBUG

def get_index():
	'''All search indexes for models should call this function as their super class.'''
	
	if DEBUG:
		return RealTimeSearchIndex
	try:
		from queued_search.indexes import QueuedSearchIndex
		return QueuedSearchIndex
	except:
		return RealTimeSearchIndex
	
haystack.autodiscover()


