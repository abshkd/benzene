import haystack
from haystack.indexes import RealTimeSearchIndex
from queued_search.indexes import QueuedSearchIndex
from settings input DEBUG

haystack.autodiscover()

def get_index():
	'''All search indexes for models should call this function as their super class.'''
	
	if DEBUG:
		return RealTimeSearchIndex
	return QueuedSearchIndex

