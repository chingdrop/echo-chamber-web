import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from rest_framework import viewsets

from .models import GoogleSearchConfig, GoogleSearchResult
from .serializers import GoogleSearchConfigSerializer, GoogleSearchResultSerializer
from crawler.tasks import run_spider


class CrawlView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            term = data['term']
            results = data['results']
            safe = data['safe']
            lang = data['lang']
            region = data['region']
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            return HttpResponseBadRequest(f"Invalid JSON data: {e}")

        
        config = GoogleSearchConfig.objects.create(
            term=term,
            results=results,
            safe=safe,
            lang=lang,
            region=region
        )

        run_spider.delay(term, config.id, results, safe, lang, region)
        return JsonResponse({'status': 'success', 'config_id': config.id})


class GoogleSearchConfigViewSet(viewsets.ModelViewSet):
    queryset = GoogleSearchConfig.objects.all()
    serializer_class = GoogleSearchConfigSerializer


class GoogleSearchResultViewSet(viewsets.ModelViewSet):
    queryset = GoogleSearchResult.objects.all()
    serializer_class = GoogleSearchResultSerializer