from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CrawlConfigViewSet, CrawlHistoryViewSet, CrawlResultViewSet


router = DefaultRouter()
router.register(r'config', CrawlConfigViewSet)
router.register(r'history', CrawlHistoryViewSet)
router.register(r'result', CrawlResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]