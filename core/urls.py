from django.urls import path
from .views import (
    TechnologiesRetrieveUpdateDestroy,
    TechnologiesListCreate,
    CategoriesListCreate,
    CategoriesRetrieveUpdateDestroy,
    RolesRetrieveUpdateDestroy,
    RolesListCreate,
    SynonymsListCreate,
    SynonymsRetrieveUpdateDestroy, RoleListingsCountListCreate, RoleListingsCountRetrieveUpdateDestroy,
    get_jobs_count_for_role,
)

# Main URL pattern the includes all router URLS's
urlpatterns = [
    path(
        "get-jobs-count-for-role/",
        get_jobs_count_for_role,
        name="get_jobs_count_for_role",
    ),
    path(
        "technologies/",
        TechnologiesListCreate.as_view(),
        name="technologies_list_create",
    ),
    path(
        "technologies/<int:pk>",
        TechnologiesRetrieveUpdateDestroy.as_view(),
        name="technologies_details",
    ),
    path("categories/", CategoriesListCreate.as_view(), name="categories_list_create"),
    path(
        "categories/<int:pk>",
        CategoriesRetrieveUpdateDestroy.as_view(),
        name="categories_details",
    ),
    path("roles/", RolesListCreate.as_view(), name="roles_list_create"),
    path("roles/<int:pk>", RolesRetrieveUpdateDestroy.as_view(), name="roles_details"),
    path("synonyms/", SynonymsListCreate.as_view(), name="synonyms_list_create"),
    path(
        "synonyms/<int:pk>",
        SynonymsRetrieveUpdateDestroy.as_view(),
        name="synonyms_details",
    ),
    path(
        "role-listings/",
        RoleListingsCountListCreate.as_view(),
        name="role_listings_count_list_create",
    ),
    path(
        "role-listings/<int:pk>",
        RoleListingsCountRetrieveUpdateDestroy.as_view(),
        name="role_listings_details",
    ),
]
