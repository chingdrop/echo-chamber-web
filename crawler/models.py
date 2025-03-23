from django.db import models
from django.utils import timezone
    

class GoogleSearchConfig(models.Model):
    term = models.CharField(max_length=255)
    results = models.IntegerField()
    safe = models.CharField(max_length=30)
    lang = models.CharField(max_length=4, blank=True, null=True)
    region = models.CharField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Google Search Configuration for {self.term}"
    

class GoogleSearchResult(models.Model):
    config = models.ForeignKey(GoogleSearchConfig, related_name="search_results", on_delete=models.CASCADE)
    link = models.URLField()
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    crawled_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Result for {self.config.term} - [{self.title}] {self.link}"