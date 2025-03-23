from rest_framework import viewsets

from .models import GoogleSearchConfig, GoogleSearchResult
from .serializers import GoogleSearchConfigSerializer, GoogleSearchResultSerializer


class GoogleSearchConfigViewSet(viewsets.ModelViewSet):
    queryset = GoogleSearchConfig.objects.all()
    serializer_class = GoogleSearchConfigSerializer


class GoogleSearchResultViewSet(viewsets.ModelViewSet):
    queryset = GoogleSearchResult.objects.all()
    serializer_class = GoogleSearchResultSerializer