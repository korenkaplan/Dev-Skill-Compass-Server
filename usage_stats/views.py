from rest_framework import generics
from .models import HistoricalTopTechnologies, TechnologiesCounts
from .serializers import HistoricalTopTechnologiesSerializer, TechnologyCountSerializer


class HistoricalTopTechnologiesListCreate(generics.ListCreateAPIView):
    queryset = HistoricalTopTechnologies.objects.all()
    serializer_class = HistoricalTopTechnologiesSerializer


class HistoricalTopTechnologiesRetrieveUpdateDestroy(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = HistoricalTopTechnologies.objects.all()
    serializer_class = HistoricalTopTechnologiesSerializer


class TechnologicalCountListCreate(generics.ListCreateAPIView):
    queryset = TechnologiesCounts.objects.all()
    serializer_class = TechnologyCountSerializer


class TechnologicalCountRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TechnologiesCounts.objects.all()
    serializer_class = TechnologyCountSerializer
