from rest_framework import serializers

from .models import GoogleSearchConfig, GoogleSearchResult


class GoogleSearchConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleSearchConfig
        fields = '__all__'


class GoogleSearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleSearchResult
        fields = '__all__'