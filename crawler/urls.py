from django.urls import path
from django.http import HttpRequest

from . import views


urlpatterns = [
    path(
        route='start',
        view=views.start_crawl,
        name='start_crawl'
    ),
]

app_name = 'crawler'