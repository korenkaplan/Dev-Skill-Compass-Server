from django.urls import path
from .views import (TechnologiesRetrieveUpdateDestroy, TechnologiesListCreate,
                    CategoriesListCreate, CategoriesRetrieveUpdateDestroy,
                    RolesRetrieveUpdateDestroy, RolesListCreate, SynonymsListCreate, SynonymsRetrieveUpdateDestroy)

# Main URL pattern the includes all router URLS's
urlpatterns = [
    path('technologies/', TechnologiesListCreate.as_view(), name='technologies_list_create'),
    path('technologies/<int:pk>', TechnologiesRetrieveUpdateDestroy.as_view(), name='technologies_details'),

    path('categories/', CategoriesListCreate.as_view(), name='categories_list_create'),
    path('categories/<int:pk>', CategoriesRetrieveUpdateDestroy.as_view(), name='categories_details'),

    path('roles/', RolesListCreate.as_view(), name='roles_list_create'),
    path('roles/<int:pk>', RolesRetrieveUpdateDestroy.as_view(), name='roles_details'),

    path('synonyms/', SynonymsListCreate.as_view(), name='synonyms_list_create'),
    path('synonyms/<int:pk>', SynonymsRetrieveUpdateDestroy.as_view(), name='synonyms_details'),
]
