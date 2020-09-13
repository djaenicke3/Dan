from django.shortcuts import render,HttpResponse,redirect
from .models import NewsList
from .forms import NameForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User






# Create your views here.
def home(request):

	rows=NewsList.objects.all()
	# if this is a POST request we need to process the form data


	form = NameForm(request.GET)

	rows=NewsList.objects.all()
	paginator = Paginator(rows, 25) # Show 25 contacts per page.
	page_obj=paginator.get_page(2)	
	selected_url=request.GET.get("url",'')
	key=request.GET.get('key','')
	page_num = request.GET.get('page', 1)
	if selected_url == '':
		if key == "":
			pass
		else :
				rows=NewsList.objects.filter(headline__icontains=key)
		
	else:

		if key == '':

			rows=NewsList.objects.filter(base_url=selected_url)
		else:
			rows=NewsList.objects.filter(base_url=selected_url,headline__icontains=key)
	
	paginator = Paginator(rows, 25) # Show 25 contacts per page.
	page_obj=paginator.get_page(page_num)	

	return render(request, 'first_page/articles.html', {'form': form,'rows':page_obj,'paginator':paginator,'page_num':page_num,
												'url':selected_url,'key':key})

def signin(request):
	if request.method == 'POST':
		print(request.POST)
		username=request.POST.get('name')
		email=request.POST.get('email')
		password=request.POST.get('pass')
		user=User.objects.create_user(username,email,password)
		user.save()

		return redirect('login')
	else:
		return render(request,'first_page/signin.html')



def login(request):
	#username = request.POST['username']
	#password = request.POST['password']
	user = None#authenticate(request, username=username, password=password)
	if user is not None:
		home(request,user)
		# Redirect to a success page.
		...
	else:
		# Return an 'invalid login' error message.
		...

	return render(request,'first_page/login.html')

def about(request):
	num=request.session.get('num',0)+1
	request.session['num']=num
	if num>4:
		del(request.session['num'])
	return HttpResponse(f'view count ={num}')
