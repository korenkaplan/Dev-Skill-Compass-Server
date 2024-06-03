from rest_framework import serializers
from .models import MonthlyTechnologiesCounts, HistoricalTechCounts, AggregatedTechCounts


class MonthlyTechnologyCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyTechnologiesCounts
        fields = "__all__"


class MonthlyHistoricalTopTechnologiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalTechCounts
        fields = "__all__"


class AggregatedTechCountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AggregatedTechCounts
        fields = "__all__"
