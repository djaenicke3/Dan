from django.shortcuts import render, HttpResponse
from .models import NewsList
from .forms import NameForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import connection


def is_valid_queryparam(param):
    return param != '' and param is not None


def timeline(request):
    rows = NewsList.objects.all()
    date_min = request.GET.get('date_min', '')
    date_max = request.GET.get('date_max', '')
    selected_url = request.GET.get("url", '')
    page_num = request.GET.get('page', 1)

    total_number = NewsList.objects.all().count()

    if is_valid_queryparam(date_min):
        rows = rows.filter(published_date__gte=date_min)

    if is_valid_queryparam(date_max):
        rows = rows.filter(published_date__lt=date_max)

    categories = NewsList.objects.values_list('base_url', flat=True).distinct()
    categories = list(categories)

    rows = rows.order_by('-published_date')
    paginator = Paginator(rows, 25)  # Show 25 contacts per page.
    page_obj = paginator.get_page(page_num)

    context = {'rows': page_obj, 'date_min': date_min, 'date_max': date_max, 'total_number': total_number,
               'selected_url': selected_url}

    return render(request, 'first_page/articles.html', context)



# Create your views here.
def home(request):
    # if this is a POST request we need to process the form data

    rows = NewsList.objects.all()
    selected_url = request.GET.get("url", '')
    title_contains = request.GET.get('title_contains', '')
    date_min = request.GET.get('date_min', '')
    date_max = request.GET.get('date_max', '')
    title_or_author = request.GET.get('title_or_author', '')
    page_num = request.GET.get('page', 1)
    if selected_url == '':
        if title_contains == "":
            pass
        else:
            rows = NewsList.objects.filter(headline__icontains=title_contains)

    else:

        if title_contains == '':

            rows = NewsList.objects.filter(base_url=selected_url)
        else:
            rows = NewsList.objects.filter(base_url=selected_url, headline__icontains=title_contains)

    rows = rows.order_by('-published_date')

    cur = connection.cursor()

    # cur.execute("SELECT COUNT * from news_list")

    if is_valid_queryparam(title_or_author):
        rows = rows.filter(author__icontains=title_or_author)
    paginator = Paginator(rows, 25)  # Show 25 contacts per page.
    print(paginator.num_pages)
    categories = NewsList.objects.values_list('base_url', flat=True).distinct()
    categories = list(categories)
    page_obj = paginator.get_page(page_num)
    total_number=NewsList.objects.all().count()


    return render(request, 'first_page/articles.html',
                  {'rows': page_obj, 'paginator': paginator, 'page_num': page_num, 'total_number': total_number,
                   'url': selected_url, 'title_contains': title_contains, 'categories': categories,
                   'title_contains': title_contains, 'date_min': date_min, 'date_max': date_max,
                   'title_or_author': title_or_author})


def about(request):
    num = request.session.get('num', 0) + 1
    request.session['num'] = num
    if num > 4:
        del (request.session['num'])
    return HttpResponse(f'view count ={num}')