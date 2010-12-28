from bencode import bencode, bdecode
from django import forms
from utils import sort_dict

class UploadTorrentForm(forms.Form)
	torrent = forms.FileField()
	name = forms.CharField()
	
	def clean_torrent(self):
		cd = self.cleaned_data
		tdata = cd['torrent'].read()
		try:
			tdict = bdecode(tdata)
		except:
			raise forms.ValidationError('.torrent file is not valid')
		tdict['announce'] = 'R' #need to replace later in process
		cd['torrent'] = bencode(sort_dict(tdict))
		return cd