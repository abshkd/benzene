from django import forms

class UploadTorrentForm(forms.Form)
	torrent = forms.FileField()
	name = forms.CharField()
	
	def clean_torrent(self):
		cd = self.cleaned_data
		cd['torrent'] = cd['torrent'].read()