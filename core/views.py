from django.views.decorators.cache import cache_page
from rest_framework import generics
from .models import Technologies, Roles, Categories, Synonyms, RoleListingsCount
from .serializers import (
    TechnologySerializer,
    CategorySerializer,
    RoleSerializer,
    SynonymsSerializer, RoleListingsCountSerializer,
)


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


class RoleListingsCountRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoleListingsCount.objects.all()
    serializer_class = RoleListingsCountSerializer
