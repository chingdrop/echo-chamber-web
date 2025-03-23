from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CrawlView, GoogleSearchConfigViewSet, GoogleSearchResultViewSet


router = DefaultRouter()
router.register(r'config', GoogleSearchConfigViewSet)
router.register(r'result', GoogleSearchResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('run_spider/', CrawlView.as_view, name='run_spider'),
]