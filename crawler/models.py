from django.db import models
from django.utils import timezone
    

class GoogleSearchConfig(models.Model):
    term = models.TextField()
    results = models.IntegerField()
    lang = models.CharField(max_length=4)
    safe = models.CharField(max_length=30)
    region = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Google Search Configuration for {self.term}"
    

class GoogleSearchResult(models.Model):
    config = models.ForeignKey(GoogleSearchConfig, related_name="results", on_delete=models.CASCADE)
    link = models.URLField()
    http_status = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    crawled_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Result for {self.config.term} - [{self.title}] {self.link}"