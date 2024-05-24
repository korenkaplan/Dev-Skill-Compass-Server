from django.urls import path, include
from rest_framework import routers
from .views import (TechnologicalCountRetrieveUpdateDestroy, TechnologicalCountListCreate,
                    HistoricalTopTechnologiesListCreate, HistoricalTopTechnologiesRetrieveUpdateDestroy)


# Main URL pattern that includes all routes URL
urlpatterns = [
    path('technologiesCounts/', TechnologicalCountListCreate.as_view(), name='technologiesCounts_list_create'),
    path('technologiesCounts/<int:pk>', TechnologicalCountRetrieveUpdateDestroy.as_view(), name='technologiesCounts_details'),

    path('historicalTopTechnologies/', HistoricalTopTechnologiesListCreate.as_view(), name='historical_top_list_create'),
    path('historicalTopTechnologies/<int:pk>', HistoricalTopTechnologiesRetrieveUpdateDestroy.as_view(), name='historical_top_details'),
]
