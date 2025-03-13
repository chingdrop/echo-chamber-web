from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'results', views.ResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(route='start/', view=views.start_crawl, name='start_crawl'),
]