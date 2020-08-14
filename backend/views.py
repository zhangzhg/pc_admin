from django.http import JsonResponse
from django.core.cache import cache
from django.db.models import Min
from urllib import request, parse
from django.views.decorators.http import require_http_methods
from scrapy.http import HtmlResponse
from .services.searchSpider import SearchSpider
from django.core import serializers
from .models import BookChapter
from .models import BookItem
from pc_admin.settings import ROOT_URL
import requests
import json
import time

'''
查询书籍
'''


@require_http_methods(["GET"])
def search(r):
    response = {}
    try:
        url = ROOT_URL + '/modules/article/waps.php'
        params = {'searchkey': r.GET.get('name')}
        data = bytes(parse.urlencode(params), 'UTF-8')
        req = request.Request(url=url, data=data, method='POST')
        req.add_header('User-Agent', r.headers['User-Agent'])
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        res = request.urlopen(req)
        # 获取所以列表
        # books = BookIndex.objects.filter()b

        res2 = HtmlResponse(url=url, body=res.read(), encoding='utf-8')
        spider = SearchSpider(res2)
        books = spider.doList()
        response['data'] = json.loads(serializers.serialize("json", books))
        response['success'] = 1
        res.close()
    except Exception as e:
        response['success'] = 0
        # 输出错误信息
        response['msg'] = str(e)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@require_http_methods(["GET"])
def findChapterList(r):
    response = {}
    try:
        name = r.GET.get('name')
        chapters = BookChapter.objects.filter(name=name)
        response['data'] = json.loads(serializers.serialize("json", chapters))
        response['success'] = 1
    except Exception as e:
        response['success'] = 0
        # 输出错误信息
        response['msg'] = str(e)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@require_http_methods(["GET"])
def getChapterList(r):
    url = r.GET.get('url')
    url = parse.unquote(url)
    cv = cache.get(url)
    if cv is None:
        spider = 'http://localhost:6800/schedule.json'
        data = {'project': 'book', 'spider': 'chapter', 'u': url}
        requests.post(url=spider, data=data)
        cache.set(url, 1, 3600)
    return findChapterList(r)


@require_http_methods(["GET"])
def getContent(r):
    url = r.GET.get('url')
    url = ROOT_URL + parse.unquote(url)
    result = getText(url)
    if result['success'] == 0:
        cv = cache.get(url)
        if cv is None:
            title = r.GET.get('title')
            spider = 'http://localhost:6800/schedule.json'
            data = {'project': 'book', 'spider': 'biqu', 'u': url, 't': title, 'n': 0}
            requests.post(url=spider, data=data)
            cache.set(url, 1, 20)
        time.sleep(1)
        result = getText(url)
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


@require_http_methods(["GET"])
def getAllContent(r):
    url = r.GET.get('url')
    url = ROOT_URL + parse.unquote(url)
    cv = cache.get(url)
    if cv is None:
        title = r.GET.get('title')
        count = BookChapter.objects.filter(name=title, load=0).aggregate(c=Min('count'))
        if count is not None and count['c'] is not None:
            c = count['c']
            chapter = BookChapter.objects.filter(name=title, count=c).get()
            url = ROOT_URL + chapter.url
        spider = 'http://localhost:6800/schedule.json'
        data = {'project': 'book', 'spider': 'biqu', 'u': url, 'n': 1}
        requests.post(url=spider, data=data)
        cache.set(url, 1, 120)
    result = {'success': 1}
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


def getText(url):
    response = {}
    try:
        chapters = BookItem.objects.filter(url=url)
        if len(chapters) > 0:
            response['data'] = json.loads(serializers.serialize("json", chapters))
            response['success'] = 1
        else:
            response['success'] = 0
    except Exception as e:
        response['success'] = 0
        # 输出错误信息
        response['msg'] = str(e)
    return response
