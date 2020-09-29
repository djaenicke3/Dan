from django.shortcuts import render, HttpResponse
from .models import NewsList
from .forms import NameForm
from django.db.models import Q
from django.core.paginator import Paginator


def is_valid_queryparam(param):
    return param != '' and param is not None


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

    if is_valid_queryparam(date_min):
        rows = rows.filter(published_date__gte=date_min)

    if is_valid_queryparam(date_max):
        rows = rows.filter(published_date__lt=date_max)
    if is_valid_queryparam(title_or_author):
        rows = rows.filter(author__icontains=title_or_author)
    paginator = Paginator(rows, 25)  # Show 25 contacts per page.
    print(paginator.num_pages)
    categories = NewsList.objects.values_list('base_url', flat=True).distinct()
    categories = list(categories)
    page_obj = paginator.get_page(page_num)

    return render(request, 'first_page/articles.html', {'rows': page_obj, 'paginator': paginator, 'page_num': page_num,
                                                        'url': selected_url, 'title_contains': title_contains,
                                                        'categories': categories,
                                                        'title_contains': title_contains, 'date_min': date_min,
                                                        'date_max': date_max, 'title_or_author': title_or_author})
