from rest_framework import generics
from rest_framework.response import Response
from core.models import Roles
from utils.settings import CACHE_TTL
from .models import HistoricalTechCounts, MonthlyTechnologiesCounts, AggregatedTechCounts
from .serializers import (MonthlyHistoricalTopTechnologiesSerializer, MonthlyTechnologyCountSerializer,
                          AggregatedTechCountsSerializer)
from rest_framework.decorators import api_view
from .services.aggregated_tech_counts_service import (get_last_scan_date_and_time, get_role_count_stats)
from django.core.cache import cache
from core.serializers import RoleSerializer


@api_view(['Get'])
def get_all_roles(request):
    cache_key = 'all_roless'
    cache_result = cache.get(cache_key)

    if cache_result:
        return Response(cache_result, 200)

    result = Roles.objects.all()
    serializer = RoleSerializer(result, many=True)
    cache.set(cache_key, serializer.data, timeout=CACHE_TTL)

    return Response(serializer.data, 200)


@api_view(['Post'])
def get_role_count_stats_view(request):
    # get the params from body
    number_of_categories = request.data.get('number_of_categories')
    limit = request.data.get('limit')
    all_categories_limit = request.data.get('all_categories_limit')
    role_id = request.data.get('role_id')

    # Define a cache key based on the input parameters
    cache_key = f"role_stats_{role_id}_{number_of_categories}_{limit}_{all_categories_limit}"

    # Check if the data is already cached
    cached_result = cache.get(cache_key)
    if cached_result:
        return Response({'data': cached_result}, status=200)

    # If not cached, call the function
    result = get_role_count_stats(role_id, number_of_categories, limit,
                                  all_categories_limit)

    # Cache the result for future requests (adjust the timeout as needed)
    cache.set(cache_key, result, timeout=CACHE_TTL)  # Cache for 1 hour

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
