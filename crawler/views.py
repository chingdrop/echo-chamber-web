from rest_framework import viewsets

from .models import CrawlConfig, CrawlHistory, CrawlResult
from .serializers import CrawlConfigSerializer, CrawlHistorySerializer, CrawlResultSerializer


class CrawlConfigViewSet(viewsets.ModelViewSet):
    queryset = CrawlConfig.objects.all()
    serializer_class = CrawlConfigSerializer


class CrawlHistoryViewSet(viewsets.ModelViewSet):
    queryset = CrawlHistory.objects.all()
    serializer_class = CrawlHistorySerializer


class CrawlResultViewSet(viewsets.ModelViewSet):
    queryset = CrawlResult.objects.all()
    serializer_class = CrawlResultSerializer