from rest_framework import serializers

from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'crawl_name', 'target_link', 'results_json']