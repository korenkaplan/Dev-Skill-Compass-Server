from django.urls import path
from .views import (
    TechnologicalCountRetrieveUpdateDestroy,
    TechnologicalCountListCreate,
    HistoricalTopTechnologiesListCreate,
    HistoricalTopTechnologiesRetrieveUpdateDestroy,
    AggregatedTechCountsListCreate,
    AggregatedTechCountsRetrieveUpdateDestroy, get_top_by_role_view, get_top_counts_for_all_roles_view,
    get_last_scan_date_and_time_view
)


# Main URL pattern that includes all routes URL
urlpatterns = [
    path(
        "get-top-by-role-view/",
        get_top_by_role_view,
        name="get_top_by_role_view",
    ),
    path(
        "get-last-scan-date-and-time-view/",
        get_last_scan_date_and_time_view,
        name="get_last_scan_date_and_time_view",
    ),
    path(
        "get-top-counts-for-all-roles-view/",
        get_top_counts_for_all_roles_view,
        name="get_top_counts_for_all_roles_view",
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
