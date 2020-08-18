from django import forms
from .rss_urls import urls
from .models import NewsList



rss= [(x,x) for x in urls]
class NameForm(forms.Form):
    url = forms.CharField(label='      Select a url :',required=False,widget=forms.Select(choices=rss,attrs={'class':'form-control'}))
    
    key=forms.CharField(label='Enter a search key :', max_length=100,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))



			
		