from rest_framework import serializers
from .models import TechnologyCount, HistoricalTopTechnologies
from core.serializers import TechnologySerializer, RoleSerializer


class TechnologyCountSerializer(serializers.ModelSerializer):
    technology = TechnologySerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    class Meta:
        model = TechnologyCount
        fields = '__all__'


class HistoricalTopTechnologiesSerializer(serializers.ModelSerializer):
    technology = TechnologySerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    class Meta:
        model = HistoricalTopTechnologies
        fields = '__all__'
