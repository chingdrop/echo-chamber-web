from rest_framework import serializers

from .models import CrawlConfig, CrawlHistory, CrawlResult


class CrawlConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlConfig
        fields = '__all__'


class CrawlHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlHistory
        fields = '__all__'


class CrawlResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlResult
        fields = '__all__'