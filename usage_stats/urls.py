from django.urls import path
from .views import (
    TechnologicalCountRetrieveUpdateDestroy,
    TechnologicalCountListCreate,
    HistoricalTopTechnologiesListCreate,
    HistoricalTopTechnologiesRetrieveUpdateDestroy,
    AggregatedTechCountsListCreate,
    AggregatedTechCountsRetrieveUpdateDestroy
)


# Main URL pattern that includes all routes URL
urlpatterns = [
    path(
        "technologiesCounts/",
        TechnologicalCountListCreate.as_view(),
        name="technologiesCounts_list_create",
    ),
    path(
        "technologiesCounts/<int:pk>",
        TechnologicalCountRetrieveUpdateDestroy.as_view(),
        name="technologiesCounts_details",
    ),
    path(
        "historicalTopTechnologies/",
        HistoricalTopTechnologiesListCreate.as_view(),
        name="historical_top_list_create",
    ),
    path(
        "historicalTopTechnologies/<int:pk>",
        HistoricalTopTechnologiesRetrieveUpdateDestroy.as_view(),
        name="historical_top_details",
    ),
    path(
        "aggregatedTechCounts/",
        AggregatedTechCountsListCreate.as_view(),
        name="historical_top_list_create",
    ),
    path(
        "aggregatedTechCounts/<int:pk>",
        AggregatedTechCountsRetrieveUpdateDestroy.as_view(),
        name="historical_top_details",
    ),
]
