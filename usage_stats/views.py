from rest_framework import viewsets
from .models import HistoricalTopTechnologies, TechnologyCount
from .serializers import HistoricalTopTechnologiesSerializer, TechnologyCountSerializer


class HistoricalTopTechnologiesViewSet(viewsets.ModelViewSet):
    queryset = HistoricalTopTechnologies.objects.all()
    serializer_class = HistoricalTopTechnologiesSerializer


class TechnologicalCountViewSet(viewsets.ModelViewSet):
    queryset = TechnologyCount.objects.all()
    serializer_class = TechnologyCountSerializer
