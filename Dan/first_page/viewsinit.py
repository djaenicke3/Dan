from django.shortcuts import render,HttpResponse
from .models import NewsList
from .forms import NameForm
from django.db.models import Q
from django.core.paginator import Paginator




# Create your views here.
def home(request):

	rows=NewsList.objects.all()
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		form = NameForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			
			selected_url=form.cleaned_data['url']
			key=form.cleaned_data['key']

			if selected_url == '':
				if key == None:

			
					return render(request, 'first_page/name.html', {'form': form,'rows':page_obj})


				else :
					rows=NewsList.objects.filter(headline__contains=key)
			
			else:

				if key == None:

					rows=NewsList.objects.filter(base_url=selected_url)
				else:
					rows=NewsList.objects.filter(base_url=selected_url,headline__contains=key)
		
			paginator = Paginator(rows, 25) # Show 25 contacts per page.
			page_obj=paginator.get_page(2)	

			return render(request, 'first_page/name.html', {'form': form,'rows':page_obj})

	# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm()
		rows=NewsList.objects.all()
		paginator = Paginator(rows, 25) # Show 25 contacts per page.
		page_obj=paginator.get_page(2)	

		#print(cursor.fetchall())

	return render(request, 'first_page/name.html', {'form': form,'rows':page_obj})