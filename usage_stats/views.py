from rest_framework import generics
from rest_framework.response import Response

from decorators.chcek_parameters import check_parameters
from .models import HistoricalTechCounts, MonthlyTechnologiesCounts, AggregatedTechCounts
from .serializers import (MonthlyHistoricalTopTechnologiesSerializer, MonthlyTechnologyCountSerializer,
                          AggregatedTechCountsSerializer)
from rest_framework.decorators import api_view

from .services.aggregated_tech_counts_service import get_top_category_for_role, get_top_by_category_role


@api_view(['Post'])
@check_parameters('role', 'categories')
def get_top_by_category_role_view(request):
    # get the params from body
    role = request.data.get('role')
    category = request.data.get('categories')
    limit = request.data.get('limit')
    # Call the function
    items = get_top_by_category_role(role, category, limit)
    # Return the results
    body = {
        'data': items
    }
    return Response(body, status=200)


@api_view(['Get'])
def hello_world(request):
    # get the role
    role = request.query_params.get('role', None)
    if role is None:
        return Response({'error': 'Role parameter is required'}, status=400)

    items = get_top_category_for_role(role=role)

    return Response({'data': items})


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
