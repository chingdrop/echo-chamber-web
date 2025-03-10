from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Result
from .serializers import ResultSerializer
from crawler.tasks import crawl_website


@api_view(['GET'])
def start_crawl(request):
    crawl_website('https://healthishot.co')
    return Response({'message': 'Test function view!'})


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
