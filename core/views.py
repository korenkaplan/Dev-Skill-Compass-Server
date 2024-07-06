from rest_framework import generics
from django.core.cache import cache
from rest_framework.response import Response
from usage_stats.management.commands.run_daily_pipeline import daily_pipeline
from usage_stats.management.commands.run_monthly_pipeline import monthly_pipeline
from utils.functions import retry_function
from utils.settings import CACHE_TTL
from .models import Technologies, Roles, Categories, Synonyms, RoleListingsCount
from .serializers import (
    TechnologySerializer,
    CategorySerializer,
    RoleSerializer,
    SynonymsSerializer, RoleListingsCountSerializer,
)
from .services.role_listings_count_services import get_job_listings_counts_from_last_number_of_months
from dotenv import load_dotenv
from memory_profiler import profile
import concurrent.futures
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os
load_dotenv()


@profile
@api_view(['Post'])
def trigger_monthly_pipeline(request):
    password = request.data.get('trigger_key')
    try:
        if password == os.environ.get('TRIGGER_KEY'):
            retry_function(monthly_pipeline, role_name='monthly_pipeline')
            return Response('run_monthly_pipeline command executed', status=401)
        else:
            return Response('Trigger key is not valid', status=200)
    except Exception as e:
        return Response(f'Error Running DailyPipline{e}', status=400)


@profile
@api_view(['POST'])
def trigger_daily_pipeline(request):
    password = request.data.get('trigger_key')
    try:
        if password == os.environ.get('TRIGGER_KEY'):
            # Execute daily_pipeline asynchronously
            with concurrent.futures.ThreadPoolExecutor() as executor:

                executor.submit(daily_pipeline)
                # Return a response immediately
                return JsonResponse({'message': 'Daily pipeline triggered successfully.'})
        else:
            return JsonResponse({'error': 'Trigger key is not valid'}, status=401)
    except Exception as e:
        return JsonResponse({'error': f'Error Running Daily Pipeline: {e}'}, status=400)


@api_view(['Get'])
def get_jobs_count_for_role(request):
    role_id: int = request.GET.get('role_id')
    cache_key = f"get_jobs_count_for_role_{role_id}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return Response(cached_result, status=200)

    result = get_job_listings_counts_from_last_number_of_months(role_id)

    cache.set(cache_key, result, timeout=CACHE_TTL)
    return Response(result, status=200)


class TechnologiesListCreate(generics.ListCreateAPIView):
    queryset = Technologies.objects.all()
    serializer_class = TechnologySerializer


class TechnologiesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Technologies.objects.all()
    serializer_class = TechnologySerializer


class CategoriesListCreate(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class CategoriesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class RolesListCreate(generics.ListCreateAPIView):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer


class RolesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer


class SynonymsListCreate(generics.ListCreateAPIView):
    queryset = Synonyms.objects.all()
    serializer_class = SynonymsSerializer


class SynonymsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Synonyms.objects.all()
    serializer_class = RoleSerializer


class RoleListingsCountListCreate(generics.ListCreateAPIView):
    queryset = RoleListingsCount.objects.all()
    serializer_class = RoleListingsCountSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        role_id = self.request.query_params.get('role_id', None)
        if role_id is None:
            return queryset
        return queryset.filter(role_id=role_id)


class RoleListingsCountRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoleListingsCount.objects.all()
    serializer_class = RoleListingsCountSerializer
