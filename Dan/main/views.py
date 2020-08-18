from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def home(request):
	return HttpResponse("<h1> Hello there! </h1>")