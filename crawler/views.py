import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from rest_framework import viewsets
from celery import chord

from .models import GoogleSearchConfig, GoogleSearchResult
from .serializers import GoogleSearchConfigSerializer, GoogleSearchResultSerializer
from crawler.tasks import google_search_task, process_search_results_task


class CrawlView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            term = data["term"]
            results = data["results"]
            safe = data["safe"]
            lang = data["lang"]
            region = data["region"]
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            return HttpResponseBadRequest(f"Invalid JSON data: {e}")

        config = GoogleSearchConfig.objects.create(
            term=term, results=results, safe=safe, lang=lang, region=region
        )

        # Create a chord with the google_search_task and a callback to process the results
        search_chord = chord(
            google_search_task.s(term, results, safe, 0, lang, region) for _ in range(1)
        )(process_search_results_task.s(config.id))

        return JsonResponse({"status": "success", "config_id": config.id})


class GoogleSearchConfigViewSet(viewsets.ModelViewSet):
    queryset = GoogleSearchConfig.objects.all()
    serializer_class = GoogleSearchConfigSerializer


class GoogleSearchResultViewSet(viewsets.ModelViewSet):
    queryset = GoogleSearchResult.objects.all()
    serializer_class = GoogleSearchResultSerializer
