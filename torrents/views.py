from bencode import bencode, bdecode
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from forms import TorrentUploadForm
from models import Torrent

def upload_torrent(request):
	form = TorrentUploadForm()
	if request.method == 'POST':
		form = TorrentUploadForm(request.POST, request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			t = Torrent(name=cd['name'], data=cd['torrent'])
			t.save()
			return HttpResponseRedirect('/')
	return HttpResponse('woot') #write template to include form, will need to include logic to register with shadowolf
