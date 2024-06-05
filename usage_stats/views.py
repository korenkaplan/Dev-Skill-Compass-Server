from rest_framework import generics
from rest_framework.response import Response

from decorators.chcek_parameters import check_parameters
from .models import HistoricalTechCounts, MonthlyTechnologiesCounts, AggregatedTechCounts
from .serializers import (MonthlyHistoricalTopTechnologiesSerializer, MonthlyTechnologyCountSerializer,
                          AggregatedTechCountsSerializer)
from rest_framework.decorators import api_view

from .services.aggregated_tech_counts_service import (get_top_counts_for_role,
                                                      get_top_counts_for_all_roles, get_last_scan_date_and_time)


@api_view(['Post'])
def get_top_counts_for_all_roles_view(request):
    # get the params from body
    number_of_categories = request.data.get('number_of_categories')
    limit = request.data.get('limit')
    # Call the function
    result = get_top_counts_for_all_roles(number_of_categories, limit)
    # Return the results
    body = {
        'data': result
    }
    return Response(body, status=200)


@api_view(['Post'])
@check_parameters('role')
def get_top_by_role_view(request):
    # get the params from body
    role = request.data.get('role')
    number_of_categories = request.data.get('number_of_categories')
    limit = request.data.get('limit')
    # Call the function
    result = get_top_counts_for_role(role, number_of_categories, limit)
    # Return the results
    body = {
        'data': result
    }
    return Response(body, status=200)


@api_view(['Get'])
def get_last_scan_date_and_time_view(request):
    # get the role
    date_time_json = get_last_scan_date_and_time()
    return Response({'data': date_time_json})


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
