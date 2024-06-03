from django.urls import path
from .views import (
    TechnologicalCountRetrieveUpdateDestroy,
    TechnologicalCountListCreate,
    HistoricalTopTechnologiesListCreate,
    HistoricalTopTechnologiesRetrieveUpdateDestroy,
    AggregatedTechCountsListCreate,
    AggregatedTechCountsRetrieveUpdateDestroy, hello_world, get_top_by_category_role_view
)


# Main URL pattern that includes all routes URL
urlpatterns = [
    path(
        "top-by-category-role/",
        get_top_by_category_role_view,
        name="get_top_by_category_role_view",
    ),
    path(
        "hello-world/",
        hello_world,
        name="hello_world",
    ),
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
