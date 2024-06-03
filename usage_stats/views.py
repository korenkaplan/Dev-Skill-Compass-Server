from rest_framework import generics
from .models import HistoricalTechCounts, MonthlyTechnologiesCounts, AggregatedTechCounts
from .serializers import (MonthlyHistoricalTopTechnologiesSerializer, MonthlyTechnologyCountSerializer,
                          AggregatedTechCountsSerializer)


class HistoricalTopTechnologiesListCreate(generics.ListCreateAPIView):
    queryset = HistoricalTechCounts.objects.all()
    serializer_class = MonthlyHistoricalTopTechnologiesSerializer


class HistoricalTopTechnologiesRetrieveUpdateDestroy(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = HistoricalTechCounts.objects.all()
    serializer_class = MonthlyHistoricalTopTechnologiesSerializer


class TechnologicalCountListCreate(generics.ListCreateAPIView):
    queryset = MonthlyTechnologiesCounts.objects.all()
    serializer_class = MonthlyTechnologyCountSerializer


class TechnologicalCountRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MonthlyTechnologiesCounts.objects.all()
    serializer_class = MonthlyTechnologyCountSerializer


class AggregatedTechCountsListCreate(generics.ListCreateAPIView):
    queryset = AggregatedTechCounts.objects.all()
    serializer_class = AggregatedTechCountsSerializer


class AggregatedTechCountsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AggregatedTechCounts.objects.all()
    serializer_class = AggregatedTechCountsSerializer
