from django.db import models
from django.utils import timezone


class CrawlConfig(models.Model):
    target_url = models.URLField()
    crawl_depth = models.PositiveIntegerField(default=1)
    include_external_links = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Crawl Configuration for {self.target_url}"
    

class CrawlHistory(models.Model):
    crawl_config = models.ForeignKey(CrawlConfig, related_name="history", on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[('started', 'Started'),
                                       ('in_progress', 'In-Progress'),
                                       ('completed', 'Completed'),
                                       ('failed', 'Failed')])
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    errors = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"History for {self.crawl_config.target_url} - {self.status}"


class CrawlResult(models.Model):
    crawl_config = models.ForeignKey(CrawlConfig, related_name="results", on_delete=models.CASCADE)
    page_url = models.URLField()
    http_status = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    content_snippet = models.TextField(blank=True, null=True)
    crawled_at = models.DateTimeField(default=timezone.now)
    external_links = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Crawl Result for {self.page_url}"
