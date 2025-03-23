from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets

from .models import GoogleSearchConfig, GoogleSearchResult
from .serializers import GoogleSearchConfigSerializer, GoogleSearchResultSerializer
from crawler.tasks import run_spider


class CrawlView(View):
    def post(self, request):
        data = request.POST.get('data')
        term = data['term']
        results = data['results']
        safe = data['safe']
        lang = data['lang']
        region = data['region']
        
        config = GoogleSearchConfig.objects.create(
            term=term,
            results=results,
            safe=safe,
            lang=lang,
            region=region
        )

        run_spider.delay(term, config.id, results, safe, lang, region)
        return HttpResponse('Scraping started!')


class GoogleSearchConfigViewSet(viewsets.ModelViewSet):
    queryset = GoogleSearchConfig.objects.all()
    serializer_class = GoogleSearchConfigSerializer


class GoogleSearchResultViewSet(viewsets.ModelViewSet):
    queryset = GoogleSearchResult.objects.all()
    serializer_class = GoogleSearchResultSerializer