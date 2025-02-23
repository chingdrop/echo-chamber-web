from django.shortcuts import render
from django.http import HttpResponse

from crawler.tasks import crawl_website


def start_crawl(request):
    crawl_website('https://healthishot.co')
    return HttpResponse("This is a test page from the new app!")