from django.core.paginator import Paginator
from django.shortcuts import render

from app import models


def index(request):
    ad_list = models.Ad.objects.order_by('-updated_at')
    paginator = Paginator(ad_list, 50)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, 'index.html', {'page_obj': page_obj})


# def fetch(request):
#     ad_list = Ad.objects.order_by('-updated_at')
#     paginator = Paginator(ad_list, 50)
#     page_num = request.GET.get('page')
#     page_obj = paginator.get_page(page_num)
#     return render(request, '_ad_list.html', {'page_obj': page_obj})


def counter(request):
    return render(request, 'counter.html')
