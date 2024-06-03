from rest_framework import serializers
from .models import MonthlyTechnologiesCounts, HistoricalTechCounts


class MonthlyTechnologyCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyTechnologiesCounts
        fields = "__all__"


class MonthlyHistoricalTopTechnologiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalTechCounts
        fields = "__all__"
