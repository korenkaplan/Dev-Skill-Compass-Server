from django.urls import path
from .views import (
    TechnologicalCountRetrieveUpdateDestroy,
    TechnologicalCountListCreate,
    HistoricalTopTechnologiesListCreate,
    HistoricalTopTechnologiesRetrieveUpdateDestroy,
    AggregatedTechCountsListCreate,
    AggregatedTechCountsRetrieveUpdateDestroy,
    get_last_scan_date_and_time_view, get_role_count_stats_view, get_all_roles
)


# Main URL pattern that includes all routes URL
urlpatterns = [
    path(
        "get-all-roles/",
        get_all_roles,
        name="get_all_roles",
    ),
    path(
        "get-last-scan-date-and-time-view/",
        get_last_scan_date_and_time_view,
        name="get_last_scan_date_and_time_view",
    ),
    path(
        "get-role-count-stats-view/",
        get_role_count_stats_view,
        name="get_role_count_stats_view",
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
