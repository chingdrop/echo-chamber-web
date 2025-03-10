from django.db import models


class Result(models.Model):
    crawl_name = models.CharField(max_length=125)
    target_link = models.URLField(max_length=255)
    results_json = models.JSONField()

    def __str__(self):
        return self.crawl_name