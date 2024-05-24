from rest_framework import serializers
from .models import TechnologiesCounts, HistoricalTopTechnologies


class TechnologyCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnologiesCounts
        fields = '__all__'


class HistoricalTopTechnologiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalTopTechnologies
        fields = '__all__'
