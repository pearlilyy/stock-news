import json
import os
import urllib.request
import sys
from django.shortcuts import render
from mystock import settings

from .models import Company
from django.core.paginator import Paginator
from django.db.models import Q


# def index(request):
#     # edit
#     company_list = Company.objects.all()
#     context = {'company_list': company_list}

#     return render(request, 'kospi/index.html', context)
def index(request):
    if request.method == 'GET':
        # 네이버 검색 API 예제 - 블로그 검색
        config_secret_debug = json.loads(
            open(settings.SECRET_DEBUG_FILE).read())
        client_id = config_secret_debug['NAVER']['CLIENT_ID']
        client_secret = config_secret_debug['NAVER']['CLIENT_SECRET']
        q = request.GET.get('q')
        encText = urllib.parse.quote("stock".format(q))
        url = "https://openapi.naver.com/v1/search/news?query=" + encText  # JSON result
        # url = "https://openapi.naver.com/v1/search/news.xml?query=" + encText # XML result
        api_request = urllib.request.Request(url)
        api_request.add_header("X-Naver-Client-Id", client_id)
        api_request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(api_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            # print(response_body.decode('utf-8'))
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')
            context = {
                'items': items
            }
        else:
            print("Error Code:" + rescode)
        return render(request, 'kospi/index.html', context=context)


def company(request):
    comp = Company.objects.all()
    page = request.GET.get('page', '1')
    searchwd = request.GET.get('searchwd', '')  # search word
    # search
    company_list = comp.order_by('code')
    if searchwd:
        company_list = company_list.filter(
            Q(code_icontains=searchwd) | Q(company_icontains=searchwd)
        ).distinct()

    # paging
    paginator = Paginator(company_list, 20)
    page_obj = paginator.get_page(page)
    context = {'comp': page_obj, 'page': page, 'searchwd': searchwd}
    return render(request, 'kospi/company.html', context)


def search(request):
    if request.method == 'GET':
        # 네이버 검색 API 예제 - 블로그 검색
        config_secret_debug = json.loads(
            open(settings.SECRET_DEBUG_FILE).read())
        client_id = config_secret_debug['NAVER']['CLIENT_ID']
        client_secret = config_secret_debug['NAVER']['CLIENT_SECRET']
        q = request.GET.get('q')
        encText = urllib.parse.quote("주가".format(q))
        url = "https://openapi.naver.com/v1/search/news?query=" + encText  # JSON result
        # url = "https://openapi.naver.com/v1/search/news.xml?query=" + encText # XML result
        api_request = urllib.request.Request(url)
        api_request.add_header("X-Naver-Client-Id", client_id)
        api_request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(api_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            # print(response_body.decode('utf-8'))
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')
            context = {
                'items': items
            }
        else:
            print("Error Code:" + rescode)
        return render(request, 'kospi/search.html', context=context)
